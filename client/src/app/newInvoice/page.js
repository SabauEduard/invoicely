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
    Textarea
} from "@nextui-org/react";
import React, { useState, useEffect } from 'react';
import { Header } from '../components/header.js';

export const overDueList = [
    { id: 1, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '20050 RON', emissionDate:'2024-12-20', dueDate: '2025-01-15', importance: 'high', note:'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop']},
    { id: 2, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '50 RON', emissionDate:'2024-12-20', dueDate: '2025-01-15', importance: 'low', note:'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop'] },
    { id: 3, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '50 RON', emissionDate:'2024-12-20', dueDate: '2025-01-15', importance: 'low', note:'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop']},
    { id: 4, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '50 RON', emissionDate:'2024-12-20', dueDate: '2025-01-15', importance: 'medium', note:'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop']},
]

export const importance = [
    { label: "Low", key: "low" },
    { label: "Medium", key: "medium" },
    { label: "High", key: "high" },
]

export const status = [
    { label: "Paid", key: "paid" },
    { label: "Unpaid", key: "unpaid" },
    { label: "Overdue", key: "overdue" },
]

export default function newInvoice() {
    const [submitted, setSubmitted] = React.useState(null);
    const [dragActive, setDragActive] = React.useState(false);
    const [id, setId] = React.useState(0);
    const [file, setFile] = React.useState(null);

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
            console.log(e.dataTransfer.files)
            setId(e.dataTransfer.files);
            setFile(e.dataTransfer.files[0]);
        }
    };

    const deleteFile = (fileToBeDeleted) => {
        setFile(null);
        setId(0);
    };

    const onSubmit = (e) => {
        e.preventDefault();

        const data = Object.fromEntries(new FormData(e.currentTarget));

        setSubmitted(data);
    };

    const [options, setOptions] = useState([
        { label: "apartament", key: "apartament" },
        { label: "utilitati", key: "utilitati" },
        { label: "casa", key: "casa" },
        { label: "laptop", key: "laptop" },
    ]);
    const [selectedTags, setSelectedTags] = useState([]);

    const handleSelectionChange = (selectedKey) => {
        if (selectedKey !== null) {
            selectedTags.push(selectedKey);
            setOptions((prevOptions) =>
                prevOptions.filter((option) => option.key !== selectedKey)
            );
        }
    };

    const handleDeleteTag = (selectedTag) => {
        if (selectedTag !== null) { }
        setSelectedTags((prevTags) => prevTags.filter((tag) => tag !== selectedTag));

        setOptions((prevOptions) => [
            ...prevOptions,
            { label: selectedTag, key: selectedTag },
        ]);

        console.log("Selected Tags:", selectedTags);
        console.log(options)
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
                <div className='border-2 border-neutral-100 p-6 flex items-center rounded-2xl'>
                    <Form className="w-full" validationBehavior='native' onSubmit={onSubmit}>
                        <div className='w-full h-full flex gap-20'>
                            <div className="flex flex-col flex-1 items-end space-y-6">
                                <div className='w-full space-y-4'>
                                    <h1 className='text-gray-500 font-medium text-base'>INVOICE DETAILS</h1>
                                    <div className='space-y-5 w-full'>
                                        <div className="flex w-full md:flex-nowrap mb-6 md:mb-0 gap-4">
                                            <Input isRequired radius='lg' name='vendor' className='w-full' size='sm' label="Vendor" type='text' />
                                            <Input isRequired radius='lg' name='amount' className='w-full' size='sm' label="Amount (RON)" type='number' />
                                        </div>
                                        <div className="flex w-full flex-wrap md:flex-nowrap gap-4">
                                            <Autocomplete radius='lg' className="w-full" name='importance' size='sm' isRequired label="Importance">
                                                {importance.map((importance) => (
                                                    <AutocompleteItem key={importance.key}>{importance.label}</AutocompleteItem>
                                                ))}
                                            </Autocomplete>
                                            <Autocomplete radius='lg' className="w-full" name='status' size='sm' isRequired label="Status">
                                                {status.map((status) => (
                                                    <AutocompleteItem key={status.key}>{status.label}</AutocompleteItem>
                                                ))}
                                            </Autocomplete>
                                        </div>
                                    </div>
                                </div>
                                <div className='w-full space-y-4'>
                                    <h1 className='text-gray-500 font-medium text-base'>DATES</h1>
                                    <div className="flex w-full md:flex-nowrap mb-6 md:mb-0 gap-4">
                                        <DatePicker className='w-full' radius='lg' name='emissionDate' size='sm' isRequired label='Emission Date' />
                                        <DatePicker className='w-full' radius='lg' name='dueDate' size='sm' isRequired label='Due Date' />
                                    </div>
                                </div>
                                <div className='w-full space-y-4'>
                                    <h1 className='text-gray-500 font-medium text-base'>DETAILS</h1>
                                    <div className="flex w-full md:flex-nowrap mb-6 md:mb-0 gap-4">
                                        <Input radius='lg' name='name' className='w-full' size='sm' isRequired label="Name" type='text' />
                                        <Autocomplete radius='lg' className="w-full" name='tags' size='sm' label="Tags" onSelectionChange={handleSelectionChange}>
                                            {options.map((option) => (
                                                <AutocompleteItem key={option.key}>{option.label}</AutocompleteItem>
                                            ))}
                                        </Autocomplete>
                                    </div>
                                </div>
                                <div className='w-full'>
                                    <Textarea
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
                                        <input
                                            type="file"
                                            className="hidden"
                                            onChange={(e) => {
                                                setId(e.target.files);
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