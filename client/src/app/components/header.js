import React, { useState } from "react";
import {
    Badge,
    Button,
    Popover,
    PopoverTrigger,
    PopoverContent,
    Divider,
    Chip,
    Drawer,
    DrawerContent,
    DrawerHeader,
    DrawerBody,
    DrawerFooter,
    useDisclosure,
} from "@nextui-org/react";
import Logo from "./logo";
import { NotificationIcon } from "./notifications";

export const Header = ({ ...props }) => {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const [size, setSize] = React.useState("4xl");
    const [popoverOpen, setPopoverOpen] = useState(false); // State for Popover

    const importanceColorMap = {
        low: "success",
        medium: "warning",
        high: "danger",
    };

    const handleOpenDrawer = () => {
        setPopoverOpen(false); // Close Popover when opening Drawer
        onOpen();
    };

    return (
        <div className="flex items-center justify-between w-full h-20 px-6">
            <Logo />
            <div className="flex flex-row items-center space-x-6">
                <Badge color="danger" content="9" shape="circle">
                    <Popover
                        placement="bottom-end"
                        shadow="md"
                        isOpen={popoverOpen} // Control visibility with state
                        onOpenChange={(open) => setPopoverOpen(open)} // Update state on visibility change
                    >
                        <PopoverTrigger>
                            <Button
                                isIconOnly
                                radius="full"
                                variant="light"
                                className="p-1"
                                onPress={() => setPopoverOpen(!popoverOpen)} // Toggle Popover visibility
                            >
                                <NotificationIcon className="fill-current" size={10} variant="light" />
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent>
                            <div className="max-h-96 w-96 pb-4">
                                <div className="w-full rounded-2xl flex items-center justify-center p-4">
                                    <h1 className="text-black text-lg font-semibold">Overdue Invoices</h1>
                                </div>
                                <div className="space-y-3">
                                    {props.overDueList.map((notificare) => (
                                        <div
                                            key={notificare.id}
                                            className="bg-gray-100 rounded-2xl py-3 pl-1 flex flex-row justify-between px-4 items-center"
                                        >
                                            <Chip
                                                color={importanceColorMap[notificare.importance]}
                                                size="sm"
                                                variant="dot"
                                                className="border-none"
                                            >
                                                <div className="ml-2">
                                                    <h1 className="text-black text-sm font-semibold">
                                                        {notificare.name}
                                                    </h1>
                                                    <p className="text-gray-600">{notificare.vendor}</p>
                                                </div>
                                            </Chip>
                                            <p className="text-gray-600">{notificare.amount}</p>
                                            <Button
                                                isIconOnly
                                                radius="full"
                                                variant="light"
                                                onPress={handleOpenDrawer} // Close Popover and open Drawer
                                            >
                                                <i className="fi fi-rr-eye text-lg flex items-center justify-center"></i>
                                            </Button>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </PopoverContent>
                    </Popover>
                </Badge>
                <i className="text-black fi fi-rr-user text-[25px] flex items-center"></i>
            </div>
            <Drawer isOpen={isOpen} size={size} onClose={onClose}>
                <DrawerContent>
                    {(onClose) => (
                        <>
                            <DrawerHeader className="flex flex-col gap-1">Drawer Title</DrawerHeader>
                            <DrawerBody>
                                <p>
                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam pulvinar risus non
                                    risus hendrerit venenatis. Pellentesque sit amet hendrerit risus, sed porttitor
                                    quam.
                                </p>
                                <p>
                                    Magna exercitation reprehenderit magna aute tempor cupidatat consequat elit dolor
                                    adipisicing. Mollit dolor eiusmod sunt ex incididunt cillum quis. Velit duis sit
                                    officia eiusmod Lorem aliqua enim laboris do dolor eiusmod.
                                </p>
                            </DrawerBody>
                            <DrawerFooter>
                                <Button color="danger" variant="light" onPress={onClose}>
                                    Close
                                </Button>
                                <Button color="primary" onPress={onClose}>
                                    Action
                                </Button>
                            </DrawerFooter>
                        </>
                    )}
                </DrawerContent>
            </Drawer>
        </div>
    );
};
