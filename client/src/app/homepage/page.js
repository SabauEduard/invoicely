'use client';

import Logo from '../components/logo.js';
import HomeCards from '../components/home_cards.js';
import SingleHomeCard from '../components/single_home_card.js';
import { Button, Badge } from "@nextui-org/react";
import TableContent from '../components/tableContent.js';
import { useRouter } from 'next/navigation';
import { Header } from '../components/header.js'
import React, { use, useEffect, useState } from 'react';
import api from '../api/api.js';
import { set } from 'react-hook-form';

export const overDueList = [
  { id: 1, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '20050 RON', emissionDate: '2024-12-20', dueDate: '2025-01-15', importance: 'high', note: 'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop'] },
  { id: 2, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '50 RON', emissionDate: '2024-12-20', dueDate: '2025-01-15', importance: 'low', note: 'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop'] },
  { id: 3, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '50 RON', emissionDate: '2024-12-20', dueDate: '2025-01-15', importance: 'low', note: 'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop'] },
  { id: 4, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '50 RON', emissionDate: '2024-12-20', dueDate: '2025-01-15', importance: 'medium', note: 'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop'] },
]


export const PlusIcon = ({ size = 24, width, height, ...props }) => {
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
      <g
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={1.5}
      >
        <path d="M6 12h12" />
        <path d="M12 18V6" />
      </g>
    </svg>
  );
};

async function getInvoices() {
  try {
    const response = await api.get('/invoices/', {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });

    return response.data;
  } catch (error) {
    console.log(error);
  }
}

const calculateAverageInvoiceAmount = (invoicesList) => {
  if (invoicesList.length === 0) return 0;

  const totalAmount = invoicesList.reduce((sum, invoice) => sum + invoice.amount, 0);
  return totalAmount / invoicesList.length;
};

const calculateOverDueAmount = (invoicesList) => {
  let total = 0;
  invoicesList.forEach((invoice) => {
    if (invoice.status === 'overdue') {
      total += invoice.amount;
    }
  });
  return total;
}

const calculateUnpaidTotals = (invoicesList) => {
  let total = 0;
  invoicesList.forEach((invoice) => {
    if (invoice.status === 'overdue' || invoice.status === 'unpaid') {
      total += invoice.amount;
    }
  });
  return total;
}

const calculateVendorWithMostInvoices = (invoicesList) => {
  const vendorCount = {};

  invoicesList.forEach((invoice) => {
    const vendor = invoice.vendor;
    if (vendorCount[vendor]) {
      vendorCount[vendor]++;
    } else {
      vendorCount[vendor] = 1;
    }
  });

  let maxCount = 0;
  let topVendor = '';

  for (const vendor in vendorCount) {
    if (vendorCount[vendor] > maxCount) {
      maxCount = vendorCount[vendor];
      topVendor = vendor;
    }
  }

  return topVendor;
}

export default function Home() {
  const router = useRouter();

  const [invoicesList, setInvoicesList] = useState(null);
  const [overDueAmount, setOverDueAmount] = useState(0);
  const [unpaidTotals, setUnpaidTotals] = useState(0);
  const [vendorWithMostInvoices, setVendorWithMostInvoices] = useState(null);
  const [averageInvoiceAmount, setAverageInvoiceAmount] = useState(0);

  useEffect(() => {
    getInvoices().then((data) => {
      setInvoicesList(data);
      setOverDueAmount(calculateOverDueAmount(data));
      setUnpaidTotals(calculateUnpaidTotals(data));
      setVendorWithMostInvoices(calculateVendorWithMostInvoices(data));
      setAverageInvoiceAmount(calculateAverageInvoiceAmount(data));
    });
  }, []);

  return (
    <div className='bg-neutral-100 min-h-screen flex relataive flex-col'>
      <Header overDueList={overDueList} />
      <div
        className="bg-white px-10 py-8 rounded-l-3xl ml-20 mb-10 space-y-8">
        <div className="w-full flex items-center justify-between">
          <h2 className='text-black text-xl font-semibold'>Invoices</h2>
          <Button color="primary" startContent={<PlusIcon />} onPress={() => router.push('/newInvoice')}>Add new invoice</Button>
        </div>
        {
          invoicesList !== null && invoicesList.length > 0 ? (
            <div className='space-x-5 flex flex-row w-full justify-center'>
              <HomeCards icon="fi-rr-alarm-exclamation" color="#DFE3C7" title="Overdue amount" text={overDueAmount.toFixed(2).toString() + " RON"} />
              <HomeCards icon="fi-rs-sack-dollar" color="#e2d5f3" title="Unpaid totals" text={unpaidTotals.toFixed(2).toString() + " RON"} />
              <HomeCards icon="fi-rr-seller" color="#f0e6e6" title="The vendor with the most invoices" text={vendorWithMostInvoices.charAt(0).toUpperCase() + vendorWithMostInvoices.slice(1)} />
              <HomeCards icon="fi-rr-payroll-calendar" color="#dce6f7" title="The average invoice cost" text={averageInvoiceAmount.toFixed(2).toString() + " RON"} />
              <SingleHomeCard totalInvoices={invoicesList.length} />
            </div>
          ) : (
            <div className='space-x-5 flex flex-row w-full justify-center'>
              <HomeCards icon="fi-rr-alarm-exclamation" color="#DFE3C7" title="Overdue amount" text="0 RON"/>
              <HomeCards icon="fi-rs-sack-dollar" color="#e2d5f3" title="Unpaid totals" text="0 RON"/>
              <HomeCards icon="fi-rr-seller" color="#f0e6e6" title="The vendor with the most invoices" text="None" />
              <HomeCards icon="fi-rr-payroll-calendar" color="#dce6f7" title="The average invoice cost" text="0 RON"/>
            </div>
          )
        }
        <div className=" p-4 rounded-2xl border-2 border-neutral-100">
          {invoicesList !== null && <TableContent invoicesList={invoicesList} />}
        </div>
      </div>
    </div>
  )
}