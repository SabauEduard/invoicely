import React, { useState } from "react";
import {
    Badge,
    Button,
    Popover,
    PopoverTrigger,
    PopoverContent,
    Chip,
} from "@nextui-org/react";
import Logo from "./logo";
import { NotificationIcon } from "./notifications";
import { DrawerComponent } from "./drawerComponent";

export const Header = ({ visibleNotification, invoicesListLength, ...props }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [selectedNotificare, setSelectedNotificare] = useState(null);
    const [size] = useState("4xl");
    const [popoverOpen, setPopoverOpen] = useState(false);
    const [notificareToSend, setNotificareToSend] = useState(null);

    const importanceColorMap = {
        low: "success",
        medium: "warning",
        high: "danger",
    };

    const handleOpenDrawer = (notificare) => {
        setPopoverOpen(false);
        setSelectedNotificare(notificare);
        setIsOpen(true);
        setNotificareToSend(notificare);
    };

    const handleCloseDrawer = () => {
        setIsOpen(false);
        setSelectedNotificare(null);
        setNotificareToSend(null);
    };

    return (
        <div className="flex items-center justify-between w-full h-20 px-6">
            <Logo />
            {visibleNotification && (
                <div className="flex flex-row items-center space-x-6">
                    {invoicesListLength ? (
                        <Badge color="danger" content={invoicesListLength} shape="circle">
                            <Popover
                                placement="bottom-end"
                                shadow="md"
                                isOpen={popoverOpen}
                                onOpenChange={(open) => setPopoverOpen(open)}
                            >
                                <PopoverTrigger>
                                    <Button
                                        isIconOnly
                                        radius="full"
                                        variant="light"
                                        className="p-1"
                                        onPress={() => setPopoverOpen(!popoverOpen)}
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
                                            {props.overDueInvoices.map((notificare) => (
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
                                                        onPress={() => handleOpenDrawer(notificare)}
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
                    ) : (
                        <NotificationIcon className="fill-current" size={10} variant="light" />
                    )
                    }
                    <i className="text-black fi fi-rr-user text-[25px] flex items-center"></i>
                </div>
            )}
            {
                notificareToSend &&
                <DrawerComponent
                    isOpen={isOpen}
                    size={size}
                    onClose={handleCloseDrawer}
                    notificare={notificareToSend}
                />
            }
        </div>
    );
};
