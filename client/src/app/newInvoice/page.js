'use client';

import Logo from '../components/logo.js';
import {
    Button,
    Input,
    Form,
    Autocomplete,
    AutocompleteItem,
    DatePicker,
    Chip,
    Textarea,
    Alert
} from "@nextui-org/react";
import React, { useState, useEffect, useRef } from 'react';
import { Header } from '../components/header.js';
import { useForm } from 'react-hook-form';
import api from '../api/api';

export const overDueList = [
    { id: 1, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '20050 RON', emissionDate: '2024-12-20', dueDate: '2025-01-15', importance: 'high', note: 'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop'] },
    { id: 2, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '50 RON', emissionDate: '2024-12-20', dueDate: '2025-01-15', importance: 'low', note: 'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop'] },
    { id: 3, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '50 RON', emissionDate: '2024-12-20', dueDate: '2025-01-15', importance: 'low', note: 'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop'] },
    { id: 4, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '50 RON', emissionDate: '2024-12-20', dueDate: '2025-01-15', importance: 'medium', note: 'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop'] },
]

export const importance = [
    { label: "low", key: "low" },
    { label: "medium", key: "medium" },
    { label: "high", key: "high" },
]

export const status = [
    { label: "paid", key: "paid" },
    { label: "unpaid", key: "unpaid" },
    { label: "overdue", key: "overdue" },
]

export default function newInvoice() {
    const [submitted, setSubmitted] = React.useState(null);
    const [dragActive, setDragActive] = React.useState(false);
    const [file, setFile] = React.useState(null);
    const [selectedTags, setSelectedTags] = useState([]);
    const [options, setOptions] = useState([
        { label: "apartament", key: "apartament" },
        { label: "utilitati", key: "utilitati" },
        { label: "casa", key: "casa" },
        { label: "laptop", key: "laptop" },
    ]);
    const initialTags = [
        { label: "apartament", key: "apartament" },
        { label: "utilitati", key: "utilitati" },
        { label: "casa", key: "casa" },
        { label: "laptop", key: "laptop" },
    ];
    const [inputValue, setInputValue] = useState('');
    const { register, watch, handleSubmit, setValue, formState: { errors } } = useForm();

    const handleDrag = function (e) {
        e.preventDefault();
        e.stopPropagation();

        if (e.type === "dragover" || e.type === "dragenter") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = function (e) {
        e.preventDefault();
        e.stopPropagation();

        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            console.log(e.dataTransfer.files[0])
            setValue("invoice", e.dataTransfer.files[0]);
            setFile(e.dataTransfer.files[0]);
        }
    };

    const deleteFile = (fileToBeDeleted) => {
        setFile(null);
    };

    const handleSelectionChange = (selectedKey) => {
        console.log("new selection", selectedKey);
        if (selectedKey !== null) {
            selectedTags.push(selectedKey);
            setOptions((prevOptions) =>
                prevOptions.filter((option) => option.key !== selectedKey)
            );
            setInputValue('');
        }
    };

    const handleSelectionChangeEnter = (e) => {
        if (e.key === "Enter" && e.target.value !== "") {
            const selectedTag = options.find(tag => tag.key === e.target.value);
            const isSubstring = options.some(tag => tag.label.includes(e.target.value));

            // if the tag is not in the tags list, add it to the selected tags
            // this prevents to add the same tag twice (one by pressing enter and one by selecting it from the list)
            if (!selectedTag && !isSubstring) {
                selectedTags.push(e.target.value);
                setOptions(options.filter(tag => tag.key !== e.target.value));
                setInputValue(''); // Resetează valoarea input-ului
            }
        }
    };

    const handleDeleteTag = (selectedTag) => {
        if (selectedTag !== null) {
            setSelectedTags((prevTags) => prevTags.filter((tag) => tag !== selectedTag));

            // if the tag was initially in the tags list, add it back (because it was one of the tags that was added previously by the user)
            // if it was added by mistake in the current session of adding a new invoice, it will not be added back 
            if (initialTags.some(tag => tag.key === selectedTag)) {
                setInputValue('');
                setOptions((prevOptions) => [
                    ...prevOptions,
                    { label: selectedTag, key: selectedTag },
                ]);
            }
        }
    };

    const formatDate = (date) => {
        const year = date.year;
        const month = String(date.month).padStart(2, '0'); // Adaugă zero la început dacă luna are o singură cifră
        const day = String(date.day).padStart(2, '0'); // Adaugă zero la început dacă ziua are o singură cifră
        return `${year}-${month}-${day}`;
    };

    const onSubmit = (data) => {
        console.log(data);
        console.log(selectedTags);

        const formData = new FormData();

        formData.append('vendor', data.vendor);
        formData.append('amount', data.amount);
        formData.append('importance', data.importance);
        formData.append('status', data.status);
        formData.append('emission_date', data.emissionDate);
        formData.append('due_date', data.dueDate);
        formData.append('name', data.name);
        formData.append('notes', data.notes);
        selectedTags.forEach(tag => formData.append('tags', tag));
        formData.append('file', data.invoice);

        const sendFormData = async () => {
            try {
                const result = await api.post('/invoices/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                    withCredentials: true,
                });



            } catch (error) {
                console.log(error);
            }

        }

        sendFormData();
    }

    useEffect(() => {
    }, [file]);

    return (
        <div className='bg-neutral-100 min-h-screen flex flex-col'>
            <Header overDueList={overDueList} />
            <div
                className="bg-white px-10 py-8 rounded-l-3xl ml-20 mb-10 space-y-8">
                <div className="w-full flex items-center justify-between">
                    <h2 className='text-black text-xl font-semibold'>Create New Invoice</h2>
                </div>
                <Alert
                    color="success"
                    description={"salut"}
                    title={"titlu"}
                    variant="faded"
                />
                <div className='border-2 border-neutral-100 p-6 flex items-center rounded-2xl'>
                    <Form className="w-full" validationBehavior='native' onSubmit={handleSubmit(onSubmit)}>
                        <div className='w-full h-full flex gap-20'>
                            <div className="flex flex-col flex-1 items-end space-y-6">
                                <div className='w-full space-y-4'>
                                    <h1 className='text-gray-500 font-medium text-base'>INVOICE DETAILS</h1>
                                    <div className='space-y-5 w-full'>
                                        <div className="flex w-full md:flex-nowrap mb-6 md:mb-0 gap-4">
                                            <Input {...register('vendor')} id='vendor' name='vendor' isRequired radius='lg' className='w-full' size='sm' label="Vendor" type='text' />
                                            {errors['vendor'] && <p className="text-[12px] text-red-800">{errors['vendor'].message}</p>}
                                            <Input {...register('amount')} id='amount' name='amount' isRequired radius='lg' className='w-full' size='sm' label="Amount (RON)" type='number' />
                                            {errors['amount'] && <p className="text-[12px] text-red-800">{errors['amount'].message}</p>}
                                        </div>
                                        <div className="flex w-full flex-wrap md:flex-nowrap gap-4">
                                            <Autocomplete {...register('importance')} id='importance' name='importance' radius='lg' className="w-full" size='sm' isRequired label="Importance">
                                                {importance.map((importance) => (
                                                    <AutocompleteItem key={importance.key}>{importance.label}</AutocompleteItem>
                                                ))}
                                            </Autocomplete>
                                            {errors['importance'] && <p className="text-[12px] text-red-800">{errors['importance'].message}</p>}
                                            <Autocomplete {...register('status')} id='status' name='status' radius='lg' className="w-full" size='sm' isRequired label="Status">
                                                {status.map((status) => (
                                                    <AutocompleteItem key={status.key}>{status.label}</AutocompleteItem>
                                                ))}
                                            </Autocomplete>
                                            {errors['status'] && <p className="text-[12px] text-red-800">{errors['status'].message}</p>}
                                        </div>
                                    </div>
                                </div>
                                <div className='w-full space-y-4'>
                                    <h1 className='text-gray-500 font-medium text-base'>DATES</h1>
                                    <div className="flex w-full md:flex-nowrap mb-6 md:mb-0 gap-4">
                                        <DatePicker {...register('emissionDate')} id='emissionDate' name='emissionDate' onChange={(date) => setValue('emissionDate', formatDate(date))} className='w-full' radius='lg' size='sm' isRequired label='Emission Date' />
                                        {errors['emissionDate'] && <p className="text-[12px] text-red-800">{errors['emissionDate'].message}</p>}
                                        <DatePicker {...register('dueDate')} id='dueDate' name='dueDate' onChange={(date) => setValue('dueDate', formatDate(date))} className='w-full' radius='lg' size='sm' isRequired label='Due Date' />
                                        {errors['dueDate'] && <p className="text-[12px] text-red-800">{errors['dueDate'].message}</p>}
                                    </div>
                                </div>
                                <div className='w-full space-y-4'>
                                    <h1 className='text-gray-500 font-medium text-base'>DETAILS</h1>
                                    <div className="flex w-full md:flex-nowrap mb-6 md:mb-0 gap-4">
                                        <Input {...register('name')} id='name' name='name' radius='lg' className='w-full' size='sm' isRequired label="Name" type='text' />
                                        {errors['name'] && <p className="text-[12px] text-red-800">{errors['name'].message}</p>}
                                        <Autocomplete selectedKey={inputValue} allowsCustomValue radius='lg' className="w-full" name='tags' size='sm' label="Tags" onKeyDown={handleSelectionChangeEnter} onSelectionChange={handleSelectionChange}>
                                            {options.map((option) => (
                                                <AutocompleteItem key={option.key}>{option.label}</AutocompleteItem>
                                            ))}
                                        </Autocomplete>
                                    </div>
                                </div>
                                <div className='w-full'>
                                    <Textarea
                                        {...register('notes')}
                                        id='notes'
                                        name='notes'
                                        isClearable
                                        className="w-full"
                                        label="Note"
                                        placeholder="Write a note for your invoice."
                                    />
                                </div>
                                <div className='w-full'>
                                    {
                                        selectedTags.length > 0 && (
                                            <div className='w-full'>
                                                <h1 className='text-gray-500 font-medium text-base'>SELECTED TAGS</h1>
                                                <div className="flex flex-wrap gap-2 pt-2">
                                                    {selectedTags.map((tag) => (
                                                        <Chip key={tag} variant="flat" onClose={() => handleDeleteTag(tag)}>
                                                            {tag}
                                                        </Chip>
                                                    ))}
                                                </div>
                                            </div>
                                        )
                                    }
                                </div>
                                <Button className='self-end' type="submit" color="primary">
                                    Submit
                                </Button>
                            </div>
                            <div className='flex-1'>
                                <div className="flex flex-col h-full">
                                    {dragActive && <div className="fixed w-screen h-screen top-0 left-0 right-0 bottom-0" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}></div>}
                                    <label
                                        onDragEnter={(e) => handleDrag(e)}
                                        style={{ backgroundColor: dragActive && "#f3f4f6" }}
                                        className="flex flex-col justify-center w-full h-full border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                                        <div className='h-full flex flex-col items-center justify-center py-2'>
                                            {
                                                file ?
                                                    file.type === 'application/pdf' ? (
                                                        <embed src={URL.createObjectURL(file)} type="application/pdf" width="100%" height="600px" />
                                                    ) : (
                                                        <img src={URL.createObjectURL(file)} alt="Selected file" />
                                                    )
                                                    : <>
                                                        <svg className="w-8 h-8 mb-4 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                                                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2" />
                                                        </svg>
                                                        <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload</span> or drag an invoice</p>
                                                    </>
                                            }
                                        </div>

                                        <Input {...register('invoice')}
                                            id='invoice'
                                            name='invoice'
                                            className='hidden'
                                            label="invoice"
                                            type='file'
                                            multiple={false}
                                            onChange={(e) => {
                                                setFile(e.target.files[0]);
                                            }}
                                        />
                                    </label>
                                </div>
                            </div>
                        </div>
                    </Form>
                </div>
            </div>
        </div>
    )
}