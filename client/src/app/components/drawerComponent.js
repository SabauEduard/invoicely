import React from "react";
import {
    Button,
    Drawer,
    DrawerContent,
    DrawerHeader,
    DrawerBody,
    DrawerFooter,
    Input,
    Textarea,
    Chip
} from "@nextui-org/react";

const formatDate = (dateString) => {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
};


export const DrawerComponent = ({ isOpen, size, onClose, notificare }) => {
    const format_emission_date = formatDate(notificare.emission_date);
    const format_due_date = formatDate(notificare.due_date);

    const serverBaseUrl = 'http://127.0.0.1:8000';
    const imagePath = `${serverBaseUrl}/${notificare.path.replace(/\\/g, '/')}`;

    return (
        notificare &&
        <Drawer isOpen={isOpen} size={size} onClose={onClose}>
            <DrawerContent>
                <>
                    <DrawerHeader className="flex flex-col gap-1 font-medium text-black text-2xl">Invoice Details</DrawerHeader>
                    <DrawerBody>
                        <div className='w-full h-full flex gap-20'>
                            <div className="flex flex-col flex-1 items-end space-y-6">
                                <div className='w-full space-y-4'>
                                    <h1 className='text-gray-500 font-medium text-base'>INVOICE DETAILS</h1>
                                    <div className='space-y-5 w-full'>
                                        <div className="flex w-full md:flex-nowrap mb-6 md:mb-0 gap-4">
                                            <Input radius='lg' readOnly name='vendor' className='w-full' size='sm' label="Vendor" value={notificare.vendor} type='text' />
                                            <Input radius='lg' readOnly name='amount' className='w-full' size='sm' label="Amount (RON)" value={notificare.amount} type='text' />
                                        </div>

                                    </div>
                                </div>
                                <div className='w-full space-y-4'>
                                    <h1 className='text-gray-500 font-medium text-base'>DATES</h1>
                                    <div className="flex w-full md:flex-nowrap mb-6 md:mb-0 gap-4">
                                        <Input className='w-full' radius='lg' name='emissionDate' readOnly value={format_emission_date} size='sm' label='Emission Date' />
                                        <Input className='w-full' radius='lg' name='dueDate' readOnly value={format_due_date} size='sm' label='Due Date' />
                                    </div>
                                </div>
                                <div className='w-full space-y-4'>
                                    <h1 className='text-gray-500 font-medium text-base'>DETAILS</h1>
                                    <div className="flex w-full md:flex-nowrap mb-6 md:mb-0 gap-4">
                                        <Input radius='lg' name='name' className='w-full' size='sm' readOnly value={notificare.name} label="Name" type='text' />
                                    </div>
                                </div>
                                <div className='w-full'>
                                    <Textarea
                                        readOnly
                                        className="w-full"
                                        label="Note"
                                        value={notificare.note}
                                    />
                                </div>
                                <div className='w-full pb-4'>
                                    <div className='w-full border-4 border-neutral-100 rounded-2xl p-2'>
                                        <h1 className='text-gray-500 font-medium text-base'>Invoice Image</h1>
                                        <img src={imagePath} alt="Invoice" className="w-full h-auto rounded-lg" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </DrawerBody>
                </>
            </DrawerContent>
        </Drawer>
    );
};
