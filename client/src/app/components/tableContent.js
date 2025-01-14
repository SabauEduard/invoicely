import React, { useEffect } from "react";
import {
    Table,
    TableHeader,
    TableColumn,
    TableBody,
    TableRow,
    TableCell,
    Input,
    Button,
    DropdownTrigger,
    Dropdown,
    DropdownMenu,
    DropdownItem,
    Chip,
    Pagination,
    DateRangePicker,
    useDisclosure,
    Modal,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
    user,
} from "@nextui-org/react";
import api from "../api/api";
import { useRouter } from "next/navigation";
import { DrawerComponent } from "./drawerComponent";
export const columns = [
    { name: "STATUS", "uid": "status", sortable: true },
    { name: "NAME", "uid": "name", sortable: true },
    { name: "CATEGORY", "uid": "category", sortable: true },
    { name: "VENDOR", "uid": "vendor", sortable: true },
    { name: "AMOUNT", "uid": "amount", sortable: true },
    { name: "IMPORTANCE", "uid": "importance", sortable: true },
    { name: "NOTE", "uid": "note" },
    // { name: "TAGS", "uid": "tags" },
    { name: "EMISSION DATE", "uid": "emission_date", sortable: true },
    { name: "DUE DATE", "uid": "due_date", sortable: true },
    { name: "ACTIONS", "uid": "actions" },
];

export const statusOptions = [
    { name: "Pending", uid: "pending" },
    { name: "Overdue", uid: "overdue" },
    { name: "Paid", uid: "paid" },
];

export const importanceOptions = [
    { name: "Low", uid: "low" },
    { name: "Medium", uid: "medium" },
    { name: "High", uid: "high" },
];

export const categoriesOptions = [
    { name: "it", uid: "it" },
    { name: "repairs", uid: "repairs" },
    { name: "consumables", uid: "consumables" },
    { name: "electricity", uid: "electricity" },
    { name: "phone", uid: "phone" },
    { name: "other", uid: "other" },
];

export function capitalize(s) {
    return s ? s.charAt(0).toUpperCase() + s.slice(1).toLowerCase() : "";
}

export const VerticalDotsIcon = ({ size = 24, width, height, ...props }) => {
    return (
        <svg
            aria-hidden="true"
            fill="none"
            focusable="false"
            height={size || height}
            role="presentation"
            viewBox="0 0 24 24"
            width={size || width}
            {...props}
        >
            <path
                d="M12 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0-6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 12c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"
                fill="currentColor"
            />
        </svg>
    );
};

export const SearchIcon = (props) => {
    return (
        <svg
            aria-hidden="true"
            fill="none"
            focusable="false"
            height="1em"
            role="presentation"
            viewBox="0 0 24 24"
            width="1em"
            {...props}
        >
            <path
                d="M11.5 21C16.7467 21 21 16.7467 21 11.5C21 6.25329 16.7467 2 11.5 2C6.25329 2 2 6.25329 2 11.5C2 16.7467 6.25329 21 11.5 21Z"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
            />
            <path
                d="M22 22L20 20"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
            />
        </svg>
    );
};

export const ChevronDownIcon = ({ strokeWidth = 1.5, ...otherProps }) => {
    return (
        <svg
            aria-hidden="true"
            fill="none"
            focusable="false"
            height="1em"
            role="presentation"
            viewBox="0 0 24 24"
            width="1em"
            {...otherProps}
        >
            <path
                d="m19.92 8.95-6.52 6.52c-.77.77-2.03.77-2.8 0L4.08 8.95"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeMiterlimit={10}
                strokeWidth={strokeWidth}
            />
        </svg>
    );
};

export const RefreshDateIcon = ({ fill = "currentColor", size, height, width, ...props }) => {
    return (
        <svg
            fill="none"
            height={size || height || 24}
            viewBox="0 0 24 24"
            width={size || width || 24}
            xmlns="http://www.w3.org/2000/svg"
            {...props}
        >
            <path
                clipRule="evenodd"
                d="M21.962,12.875A10.03,10.03,0,1,1,19.122,5H16a1,1,0,0,0-1,1h0a1,1,0,0,0,1,1h4.143A1.858,1.858,0,0,0,22,5.143V1a1,1,0,0,0-1-1h0a1,1,0,0,0-1,1V3.078A11.985,11.985,0,1,0,23.95,13.1a1.007,1.007,0,0,0-1-1.1h0A.982.982,0,0,0,21.962,12.875Z"
                fill={fill}
                fillRule="evenodd"
            />
        </svg>
    );
};


const statusColorMap = {
    paid: "success",
    pending: "warning",
    overdue: "danger",
};

const importanceColorMap = {
    low: "success",
    medium: "warning",
    high: "danger",
};

const INITIAL_VISIBLE_COLUMNS = ["name", "category", "vendor", "amount", "status", "tags", "importance", "actions"];

export default function TableContent(props) {
    const handleOpenDrawer = (notificare) => {
        console.log("DESCHIDEEEEE", notificare);
        setPopoverOpen(false);
        setSelectedNotificare(notificare);
        setIsOpenDrawer(true);
        setNotificareToSend(notificare);
    };

    const handleCloseDrawer = () => {
        setIsOpenDrawer(false);
        setSelectedNotificare(null);
        setNotificareToSend(null);
    };

    const { isOpen, onOpen, onOpenChange } = useDisclosure();

    const [isOpenDrawer, setIsOpenDrawer] = React.useState(false);
    const [selectedNotificare, setSelectedNotificare] = React.useState(null);
    const [size] = React.useState("4xl");
    const [popoverOpen, setPopoverOpen] = React.useState(false);
    const [notificareToSend, setNotificareToSend] = React.useState(null);

    const [filterValue, setFilterValue] = React.useState("");
    const [selectedKeys, setSelectedKeys] = React.useState(new Set([]));
    const [visibleColumns, setVisibleColumns] = React.useState(new Set(INITIAL_VISIBLE_COLUMNS));
    const [statusFilter, setStatusFilter] = React.useState("all");
    const [importanceFilter, setImportanceFilter] = React.useState("all");
    const [emissionDateFilter, setEmissionDateFilter] = React.useState(null);
    const [dueDateFilter, setDueDateFilter] = React.useState(null);
    const [categoryFilter, setCategoryFilter] = React.useState("all");
    const [invoices, setInvoices] = React.useState(props.invoicesList || []);
    const [openViewwer, setOpenViewer] = React.useState(false);
    const [sortDescriptor, setSortDescriptor] = React.useState({
        column: "age",
        direction: "ascending",
    });
    const [page, setPage] = React.useState(1);

    const router = useRouter();
    const hasSearchFilter = Boolean(filterValue);
    const rowsPerPage = 10;

    const headerColumns = React.useMemo(() => {
        if (visibleColumns === "all") return columns;

        return columns.filter((column) => Array.from(visibleColumns).includes(column.uid));
    }, [visibleColumns]);

    const filteredInvoices = React.useMemo(() => {
        let filteredInvoices = invoices;

        if (hasSearchFilter) {
            filteredInvoices = filteredInvoices.filter((invoice) => {
                return Object.values(invoice).some(value =>
                    value.toString().toLowerCase().includes(filterValue.toLowerCase())
                );
            });
        }
        if (statusFilter !== "all" && Array.from(statusFilter).length !== statusOptions.length) {
            filteredInvoices = filteredInvoices.filter((invoice) =>
                Array.from(statusFilter).includes(invoice.status),
            );
        }

        if (importanceFilter !== "all" && Array.from(importanceFilter).length !== importanceOptions.length) {
            filteredInvoices = filteredInvoices.filter((invoice) =>
                Array.from(importanceFilter).includes(invoice.importance),
            );
        }

        if (emissionDateFilter) {
            filteredInvoices = filteredInvoices.filter((invoice) => {
                const emissionDate = new Date(invoice.emission_date);
                const startDate = new Date(emissionDateFilter.start);
                const endDate = new Date(emissionDateFilter.end);

                return emissionDate.getTime() >= startDate.getTime() && emissionDate.getTime() <= endDate.getTime();
            });
        }

        if (dueDateFilter) {
            filteredInvoices = filteredInvoices.filter((invoice) => {
                const dueDate = new Date(invoice.due_date);
                const startDate = new Date(dueDateFilter.start);
                const endDate = new Date(dueDateFilter.end);

                return dueDate.getTime() >= startDate.getTime() && dueDate.getTime() <= endDate.getTime();
            });
        }

        if (categoryFilter !== "all" && Array.from(categoryFilter).length !== categoriesOptions.length) {
            filteredInvoices = filteredInvoices.filter((invoice) =>
                Array.from(categoryFilter).includes(invoice.category),
            );
        }

        return filteredInvoices;
    }, [invoices, filterValue, statusFilter, importanceFilter, emissionDateFilter, dueDateFilter, categoryFilter]);

    const pages = Math.ceil(filteredInvoices.length / rowsPerPage);

    const items = React.useMemo(() => {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        return filteredInvoices.slice(start, end);
    }, [page, filteredInvoices, rowsPerPage]);

    const sortedItems = React.useMemo(() => {
        return [...items].sort((a, b) => {
            const first = a[sortDescriptor.column];
            const second = b[sortDescriptor.column];
            const cmp = first < second ? -1 : first > second ? 1 : 0;

            return sortDescriptor.direction === "descending" ? -cmp : cmp;
        });
    }, [sortDescriptor, items]);

    const handleDeleteInvoice = async (id) => {
        try {
            const result = await api.delete(`/invoices/${id}`, {
                headers: {
                    'Content-Type': 'application/json',
                },
                withCredentials: true,
            });

            setInvoices((prevInvoices) => prevInvoices.filter((invoice) => invoice.id !== id));
        } catch (error) {
            console.log(error);
        }
    };

    const renderCell = React.useCallback((item, columnKey) => {
        const cellValue = item[columnKey];

        switch (columnKey) {
            case "status":
                return (
                    <Chip className="capitalize" color={statusColorMap[item.status]} size="sm" variant="flat">
                        {cellValue}
                    </Chip>
                );
            case "importance":
                return (
                    <Chip color={importanceColorMap[cellValue]} size="sm" variant="dot" className="border-none">
                        {cellValue}
                    </Chip>
                )
            case "amount":
                return cellValue + " RON";
            case "tags":
                return (
                    <div className="space-x-1">
                        {
                            (cellValue || []).map((tag) => (
                                <Chip key={tag} size="sm" variant="flat">
                                    {tag}
                                </Chip>
                            ))
                        }
                    </div>
                );
            case "actions":
                return (
                    <div className="relative flex justify-end items-center gap-2">
                        <Dropdown>
                            <DropdownTrigger>
                                <Button isIconOnly size="sm" variant="light">
                                    <VerticalDotsIcon className="text-default-300" />
                                </Button>
                            </DropdownTrigger>
                            <DropdownMenu>
                                <DropdownItem key="view" color="primary" onPress={() => { handleOpenDrawer(item) }}>View</DropdownItem>
                                <DropdownItem key="edit">Edit</DropdownItem>
                                <DropdownItem key="delete" className="text-danger" color="danger" onPress={() => handleDeleteInvoice(item.id)}>
                                    Delete
                                </DropdownItem>
                            </DropdownMenu>
                        </Dropdown>
                    </div>
                );
            default:
                return cellValue;
        }
    }, []);

    const onNextPage = React.useCallback(() => {
        if (page < pages) {
            setPage(page + 1);
        }
    }, [page, pages]);

    const onPreviousPage = React.useCallback(() => {
        if (page > 1) {
            setPage(page - 1);
        }
    }, [page]);

    const onSearchChange = React.useCallback((value) => {
        if (value) {
            setFilterValue(value);
            setPage(1);
        } else {
            setFilterValue("");
        }
    }, []);

    const onClear = React.useCallback(() => {
        setFilterValue("");
        setPage(1);
    }, []);

    const topContent = React.useMemo(() => {
        return (
            <div className="flex flex-col gap-4">
                <div className="flex justify-between gap-3 items-end">
                    <Input
                        isClearable
                        className="w-full sm:max-w-[44%]"
                        placeholder="Search an invoice..."
                        startContent={<SearchIcon />}
                        value={filterValue}
                        onClear={() => onClear()}
                        onValueChange={onSearchChange}
                    />
                    <div className="flex gap-3">
                        <Dropdown>
                            <DropdownTrigger className="hidden sm:flex">
                                <Button endContent={<ChevronDownIcon className="text-small" />} variant="flat">
                                    Status
                                </Button>
                            </DropdownTrigger>
                            <DropdownMenu
                                disallowEmptySelection
                                aria-label="Table Columns"
                                closeOnSelect={false}
                                selectedKeys={statusFilter}
                                selectionMode="multiple"
                                onSelectionChange={setStatusFilter}
                            >
                                {statusOptions.map((status) => (
                                    <DropdownItem key={status.uid} className="capitalize">
                                        {capitalize(status.name)}
                                    </DropdownItem>
                                ))}
                            </DropdownMenu>
                        </Dropdown>
                        <Dropdown>
                            <DropdownTrigger className="hidden sm:flex">
                                <Button endContent={<ChevronDownIcon className="text-small" />} variant="flat">
                                    Category
                                </Button>
                            </DropdownTrigger>
                            <DropdownMenu
                                disallowEmptySelection
                                aria-label="Table Columns"
                                closeOnSelect={false}
                                selectedKeys={categoryFilter}
                                selectionMode="multiple"
                                onSelectionChange={setCategoryFilter}
                            >
                                {categoriesOptions.map((category) => (
                                    <DropdownItem key={category.uid} className="capitalize">
                                        {capitalize(category.name)}
                                    </DropdownItem>
                                ))}
                            </DropdownMenu>
                        </Dropdown>
                        <Dropdown>
                            <DropdownTrigger className="hidden sm:flex">
                                <Button endContent={<ChevronDownIcon className="text-small" />} variant="flat">
                                    Importance
                                </Button>
                            </DropdownTrigger>
                            <DropdownMenu
                                disallowEmptySelection
                                aria-label="Table Columns"
                                closeOnSelect={false}
                                selectedKeys={importanceFilter}
                                selectionMode="multiple"
                                onSelectionChange={setImportanceFilter}
                            >
                                {importanceOptions.map((importance) => (
                                    <DropdownItem key={importance.uid} className="capitalize">
                                        {capitalize(importance.name)}
                                    </DropdownItem>
                                ))}
                            </DropdownMenu>
                        </Dropdown>
                        <Dropdown>
                            <DropdownTrigger className="hidden sm:flex">
                                <Button endContent={<ChevronDownIcon className="text-small" />} variant="flat">
                                    Columns
                                </Button>
                            </DropdownTrigger>
                            <DropdownMenu
                                disallowEmptySelection
                                aria-label="Table Columns"
                                closeOnSelect={false}
                                selectedKeys={visibleColumns}
                                selectionMode="multiple"
                                onSelectionChange={setVisibleColumns}
                            >
                                {columns.map((column) => (
                                    <DropdownItem key={column.uid} className="capitalize">
                                        {capitalize(column.name)}
                                    </DropdownItem>
                                ))}
                            </DropdownMenu>
                        </Dropdown>
                    </div>
                </div>
                <div className="w-full flex justify-between items-start">
                    <span className="text-default-400 text-small">Total {filteredInvoices.length} invoices</span>
                    <div className="flex gap-2 items-center">
                        <DateRangePicker value={emissionDateFilter} onChange={setEmissionDateFilter} className="max-w-xs" label="Emission date" />
                        <DateRangePicker value={dueDateFilter} onChange={setDueDateFilter} className="max-w-xs" label="Due date" />
                        <Button isIconOnly aria-label="Remove date" variant="light" className="rounded-full text-default-400" onPress={() => {
                            setEmissionDateFilter(null);
                            setDueDateFilter(null);
                        }}>
                            <RefreshDateIcon />
                        </Button>
                    </div>
                </div>
            </div>
        );
    }, [
        filteredInvoices,
        filterValue,
        statusFilter,
        importanceFilter,
        emissionDateFilter,
        dueDateFilter,
        categoryFilter,
        visibleColumns,
        // props.invoicesList.length,
        onSearchChange,
        hasSearchFilter,
    ]);

    const bottomContent = React.useMemo(() => {
        return (
            <div className="py-2 px-2 flex justify-between items-center">
                <span className="w-[30%] text-small text-default-400">
                    <p className="none"> </p>
                </span>
                <Pagination
                    isCompact
                    showControls
                    showShadow
                    color="primary"
                    page={page}
                    total={pages}
                    onChange={setPage}
                />
                <div className="hidden sm:flex w-[30%] justify-end gap-2">
                    <Button isDisabled={pages === 1} size="sm" variant="flat" onPress={onPreviousPage}>
                        Previous
                    </Button>
                    <Button isDisabled={pages === 1} size="sm" variant="flat" onPress={onNextPage}>
                        Next
                    </Button>
                </div>
            </div>
        );
    }, [selectedKeys, items.length, page, pages, hasSearchFilter]);

    return (
        <>
            {props.invoicesList && <Table
                isHeaderSticky
                aria-label="Example table with custom cells, pagination and sorting"
                bottomContent={bottomContent}
                bottomContentPlacement="outside"
                selectedKeys={selectedKeys}
                sortDescriptor={sortDescriptor}
                topContent={topContent}
                topContentPlacement="outside"
                onSelectionChange={setSelectedKeys}
                onSortChange={setSortDescriptor}
            >
                <TableHeader columns={headerColumns}>
                    {(column) => (
                        <TableColumn
                            key={column.uid}
                            align={column.uid === "actions" ? "center" : "start"}
                            allowsSorting={column.sortable}
                        >
                            {column.name}
                        </TableColumn>
                    )}
                </TableHeader>
                <TableBody emptyContent={"No invoices found"} items={sortedItems}
                >
                    {(item) => (
                        <TableRow key={item.id}>
                            {(columnKey) => <TableCell>{renderCell(item, columnKey)}</TableCell>}
                        </TableRow>
                    )}
                </TableBody>
            </Table>
            }
            {notificareToSend &&
                <DrawerComponent
                    isOpen={isOpenDrawer}
                    size={size}
                    onClose={handleCloseDrawer}
                    notificare={notificareToSend}
                />
            }
        </>
    );
}

