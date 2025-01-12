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

export const DrawerComponent = ({ isOpen, size, onClose, notificare }) => {

    return (
        console.log(notificare),
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
                                        <Input className='w-full' radius='lg' name='emissionDate' readOnly value={notificare.emissionDate} size='sm' label='Emission Date' />
                                        <Input className='w-full' radius='lg' name='dueDate' readOnly value={notificare.dueDate} size='sm' label='Due Date' />
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
                                        placeholder="Write a note for your invoice."
                                        value={notificare.note}
                                    />
                                </div>
                                <div className='w-full'>
                                    {
                                        notificare.tags.length > 0 && (
                                            <div className='w-full'>
                                                <h1 className='text-gray-500 font-medium text-base'>SELECTED TAGS</h1>
                                                <div className="flex flex-wrap gap-2 pt-2">
                                                    {notificare.tags.map((tag) => (
                                                        <Chip key={tag} variant="flat">
                                                            {tag}
                                                        </Chip>
                                                    ))}
                                                </div>
                                            </div>
                                        )
                                    }
                                </div>
                            </div>
                        </div>
                    </DrawerBody>
                </>
            </DrawerContent>
        </Drawer>
    );
};
