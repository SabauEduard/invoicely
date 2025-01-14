import csv
from PIL import Image, ImageFile
import pytesseract
import pdf2image
import cv2
import numpy as np
import os
from dotenv import load_dotenv
from os.path import join, dirname
from transformers import AdamW, AutoTokenizer, Trainer, TrainingArguments, AutoModel, AutoModelForQuestionAnswering, AutoModelForSequenceClassification, get_scheduler
import torch
from pathlib import Path
import pandas as pd
import evaluate
from datasets import Dataset
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

load_dotenv(join(dirname(__file__), '.env'))

print(os.getenv('TESSERACT_CMD'))
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_CMD')
poppler_path = os.getenv('POPPLER_PATH')

ImageFile.LOAD_TRUNCATED_IMAGES = True

def change_dpi(image_path: str, dpi: int = 300) -> None:
    """Change the DPI of an image to the specified value, to make sure the text has a good quality for future OCR processing

    Args:
        image_path (str): The path of the image to be processed
        dpi (int, optional): The DPI value to be set. Defaults to 300.
    """   
    # image_path = "./factura_test.jpeg"
    image = Image.open(image_path)
    image.save(image_path, dpi=(dpi,dpi))
    print("DPI-ul imaginii a fost modificat cu succes")
    
    
def normalize_image(image_path: str) -> None:
    """Normalizarea imaginii pentru a uniformiza luminozitatea și contrastul imaginii

    Args:
        image_path (str): Calea către imaginea care urmează a fi normalizată
    """
    # Citirea imaginii în format grayscale
    initial_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Normalizarea imaginii. NORM_MINMAX normalizează valorile pixelilor în intervalul [0, 255]
    img = cv2.normalize(initial_image, None, 0, 255, cv2.NORM_MINMAX)

    cv2.imwrite(image_path, img)
    
def get_image_rotation(image: np.ndarray) -> int:
    """Se obțin informații despre orientarea textului din imagine

    Args:
        image (np.ndarray): Imaginea pentru care se dorește obținerea informațiilor despre orientare

    Returns:
        int: Unghiul de rotație al imaginii
    """
    d = pytesseract.image_to_osd(image, output_type=pytesseract.Output.DICT)

    return d['rotate']

def rotate_image(image_path: str, original_file_path: str, angle: int):
    """Rotirea imaginii cu un anumit unghi

    Args:
        image_path (str): Calea către imaginea care urmează a fi rotită
        original_file_path (str): Calea către imaginea originală, pentru a o roti înapoi în cazul în care textul este rotit
        angle (int): Unghiul de rotație al imaginii
    """
    # Folosim expan=True pentru a nu pierde porțiuni din imagine în timpul rotației
    image = Image.open(image_path)
    original_image = Image.open(original_file_path)
    
    image = image.rotate(angle, expand=True)
    original_image = original_image.rotate(angle, expand=True)
    
    image.save(image_path)
    original_image.save(original_file_path)
    
def get_skew_image(image_path: str, image: np.ndarray) -> float:
    """Detectarea unghiului de înclinare a imaginii

    Args:
        image (np.ndarray): Obiectul imaginii care urmează a fi procesat

    Returns:
        float: Unghiul de înclinare al imaginii
    """
    
    # Pregătirea imaginii, copierea imaginii, conversia la grayscale, aplicarea unui filtru Gaussian și aplicarea unui threshold
    new_image = image.copy()
    gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
    # dimensiunea kernelului este 9x9, iar sigma este 0
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    
    # THRESH_BINARY_INV - transformă pixelii mai mari decât valoarea de prag în 0, iar pe cei mai mici în 255
    # THRESH_OTSU - metoda Otsu pentru a determina valoarea de prag
    threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Aplicarea dilatării pentru a uni textul în linii/paragrafe semnificative
    # Se folosește un kernel mai mare pe axa X pentru a uni caracterele într-o singură linie, anulând orice spații
    # Dar se folosește un kernel mai mic pe axa Y pentru a separa între blocurile diferite de text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(threshold, kernel, iterations=5)

    # Determinarea contururilor și sortarea lor după aria lor
    contours, _ = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)

    # Determinarea celui mai mare contur
    largestContour = contours[0]
    
    # Determinarea dreptunghiului minim care înconjoară conturul
    minAreaRect = cv2.minAreaRect(largestContour)

    box = cv2.boxPoints(minAreaRect)
    box = np.int0(box)
    cv2.drawContours(new_image,[box],0,(36,255,12), 3)
    
    # Desenarea celui mai mare contur
    cv2.drawContours(new_image, [largestContour], -1, (36,255,12), 3)
    
    # Salvarea imaginii cu conturul desenat într-un fișier nou
    # cv2.imwrite("imagine_contur_nou.png", new_image)
    # cv2.imshow('image', new_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # Extragerea unghiului de înclinare din dreptunghiul minim
    angle = minAreaRect[-1]
    
    # Determinarea unghiului de înclinare real
    if angle < -45:
        angle = 90 + angle
        return -1.0 * angle
    elif angle > 45 :
        angle = 90 - angle
        return angle
    return -1.0 * angle

def deskew_image(image: np.ndarray, angle: float) -> np.ndarray:
    """Corectarea imaginii în cazul în care aceasta este înclinată

    Args:
        image (np.ndarray): Imaginea care urmează a fi corectată
        angle (float): Unghiul de înclinare al imaginii

    Returns:
        np.ndarray: _description_
    """
    new_image = image.copy()
    
    # Se determină dimensiunile imaginii și centrul imaginii
    (h, w) = new_image.shape[:2]
    center = (w // 2, h // 2)
    
    # Se rotește imaginea în jurul centrului său
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Se obține imaginea cu înclinația corectată prin aplicarea transformării
    new_image = cv2.warpAffine(new_image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
    return new_image

def deskew(image_path: str, original_file_path: str) -> None:
    """Eliminarea înclinării sau a rotației imaginii

    Args:
        image_path (str): Calea către imaginea care urmează a fi corectată
        original_file_path (str): Calea către imaginea originală, pentru a o roti 
    """
    image = cv2.imread(image_path)
    original_image = cv2.imread(original_file_path)
    
    angle = get_skew_image(image_path, image)
    new_image = deskew_image(image, -1.0 * angle)
    fixed_original_image = deskew_image(original_image, -1.0 * angle)
    cv2.imwrite(image_path, new_image)
    cv2.imwrite(original_file_path, fixed_original_image)
    # Rotim imaginea înapoi, în cazul în care deși latura inferioară a imaginii este orizontală, textul este rotit la multiplu de 90 de grade
    
    try:
        image_rotation_angle = get_image_rotation(new_image)
        if image_rotation_angle != 0:
            rotate_image(image_path, original_file_path, -image_rotation_angle)
    except Exception as e:
        pass
    
def extract_text(image_path: str) -> str:
    """Extragerea textului din imagine

    Args:
        image_path (str): Calea către imaginea din care se extrage textul

    Returns:
        str: Textul extras din imagine
    """
    return pytesseract.image_to_string(Image.open(image_path), lang='ron')

def preprocess_image(image_path: str, original_file_path: str) -> None:
    """Funcție care prelucrează imaginea înainte de a fi extras textul din ea

    Args:
        image_path (str): Calea către imaginea care urmează a fi procesată
        original_file_path (str): Calea către imaginea originală, pentru a o roti înapoi în cazul în care textul este rotit, dar fără a-i modifica DPI-ul sau culorile
    """
    
    change_dpi(image_path)    
    normalize_image(image_path) 
    deskew(image_path, original_file_path)

def scan_pdf(image_path: str) -> None:
    """Funcție care convertește un fișier PDF într-un fișier imagine și apelează funcția de prelucrare a imaginii

    Args:
        image_path (str): Calea către fișierul PDF care urmează a fi convertit
    """
    new_image = pdf2image.convert_from_path(image_path, dpi=200, fmt='jpeg', poppler_path=poppler_path)
    image = new_image[0]
    
    # Modificarea căii pentru a salva imaginea în format .jpg
    image_path_jpg = image_path.rsplit('.', 1)[0] + '.jpg'
    
    image.save(image_path_jpg)
    return image_path_jpg

def train_model():
    train_data_csv = pd.read_csv("../SeturiDeDateFacturi/train(Train).csv", encoding='iso-8859-1')
    validate_data_csv = pd.read_csv("../SeturiDeDateFacturi/train(Validate).csv", encoding='iso-8859-1')
    evaluate_data_csv = pd.read_csv("../SeturiDeDateFacturi/train(Evaluate).csv", encoding='iso-8859-1')
    
    # Create a label encoder
    label_encoder = LabelEncoder()
    
    # Fit the label encoder and transform the labels
    train_data_csv["label"] = label_encoder.fit_transform(train_data_csv["label"])
    validate_data_csv["label"] = label_encoder.transform(validate_data_csv["label"])
    evaluate_data_csv["label"] = label_encoder.transform(evaluate_data_csv["label"])
    
    labels = label_encoder.classes_
    
    # Convert pandas DataFrames to Hugging Face datasets
    train_data = Dataset.from_pandas(train_data_csv)
    validate_data = Dataset.from_pandas(validate_data_csv)
    evaluate_data = Dataset.from_pandas(evaluate_data_csv)

    
    tokenizer = AutoTokenizer.from_pretrained("dumitrescustefan/bert-base-romanian-cased-v1")
    
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)
    
    tokenized_train_data = train_data.map(tokenize_function, batched=True)
    tokenized_validate_data = validate_data.map(tokenize_function, batched=True)
    tokenized_evaluate_data = evaluate_data.map(tokenize_function, batched=True)
    
    model = AutoModelForSequenceClassification.from_pretrained("dumitrescustefan/bert-base-romanian-cased-v1", num_labels=6)
    
    metric = evaluate.load("accuracy")
    
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)
    

    training_args = TrainingArguments(
        output_dir="test_trainer", 
        evaluation_strategy="epoch",
        num_train_epochs=1)
    
    optimizer = AdamW(
        model.parameters(), 
        lr=2e-5,
        eps=1e-8,
    )
    
    scheduler = get_scheduler(
        "linear",
        optimizer,
        num_warmup_steps=0,
        num_training_steps=len(tokenized_train_data) * training_args.num_train_epochs
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train_data,
        eval_dataset=tokenized_validate_data,
        compute_metrics=compute_metrics,
        optimizers=(optimizer, scheduler)
    )
    
    trainer.train()
    trainer.save_model("category_model_adam_2")
    
def predict_category(text: str):
    tokenizer = AutoTokenizer.from_pretrained("dumitrescustefan/bert-base-romanian-cased-v1")
    model = AutoModelForSequenceClassification.from_pretrained("ml_utils/category_model_adam") 

    inputs = tokenizer(text, truncation=True, max_length=512, return_tensors='pt')

    outputs = model(**inputs)

    predicted_category = torch.argmax(outputs.logits)

    category_names = ["altele", "consumabile", "curent", "it", "reparații", "telefonie"]
    predicted_category_name = category_names[predicted_category]
    print(predicted_category_name)
    
    return predicted_category_name
    
def detect_category(original_file_path: str, file_path: str, file_type: str):
    """Funcție care verifică tipul fișierului și apelează funcția corespunzătoare pentru a procesa fișierul înainte de a-l trimite la clasificare

    Args:
        file_path (str): Calea către fișierul care trebuie scanat
        file_type (str): Tipul fișierului care trebuie scanat (image/jpeg, application/pdf, text/plain)
    """

    if file_type.split('/')[0] == 'image':
        preprocess_image(file_path, original_file_path)
        text = extract_text(file_path)
        
    if file_type.split('/')[1] == 'pdf':
        image_path_jpg = scan_pdf(file_path)
        original_path_jpg = scan_pdf(original_file_path)
        
        preprocess_image(image_path_jpg, original_path_jpg)
        text = extract_text(image_path_jpg)
        
        os.remove(original_path_jpg)
        os.remove(image_path_jpg)
        
    if file_type.split('/')[0] == 'text':
        with open(file_path, 'r') as f:
            text = f.read()
        
    text = text.replace("ţ", "ț").replace("ş", "ș").replace("Ţ", "Ț").replace("Ş", "Ș")    
           
    # Open the file with 'utf-8' encoding
    # with open('text.txt', 'w', encoding='utf-8') as f:
    #     f.write(text.replace('\n', ' '))
    text = text.replace('\n', ' ')

    predict_category_value = predict_category(text)
    
    if predict_category_value == "altele":
        predict_category_value = "other"
    elif predict_category_value == "consumabile":
        predict_category_value = "consumables"
    elif predict_category_value == "curent":
        predict_category_value = "electricity"
    elif predict_category_value == "it":
        predict_category_value = "it"
    elif predict_category_value == "reparații":
        predict_category_value = "repair"
    elif predict_category_value == "telefonie":
        predict_category_value = "phone"
        
    return predict_category_value, text