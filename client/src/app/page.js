'use client';

import Logo from './components/logo.js';
import HomeCards from './components/home_cards.js';
import SingleHomeCard from './components/single_home_card.js';
import { Button, Badge } from "@nextui-org/react";
import TableContent from './components/tableContent.js';
import { useRouter } from 'next/navigation';
import { Header } from './components/header.js'

export const overDueList = [
  { id: 1, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '20050 RON', emissionDate:'2024-12-20', dueDate: '2025-01-15', importance: 'high', note:'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop']},
  { id: 2, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '50 RON', emissionDate:'2024-12-20', dueDate: '2025-01-15', importance: 'low', note:'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop'] },
  { id: 3, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '50 RON', emissionDate:'2024-12-20', dueDate: '2025-01-15', importance: 'low', note:'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop']},
  { id: 4, status: 'Overdue', name: 'Factura licenta windows', vendor: 'Microsoft', amount: '50 RON', emissionDate:'2024-12-20', dueDate: '2025-01-15', importance: 'medium', note:'Avem aici una bucata factura la licenta de windows nu mai umblati cu windows crackuit', tags: ['laptop']},
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

export default function Home() {
  const router = useRouter();

  return (
    <div className='bg-neutral-100 min-h-screen flex relataive flex-col'>
      <Header overDueList={overDueList} />
      <div
        className="bg-white px-10 py-8 rounded-l-3xl ml-20 mb-10 space-y-8">
        <div className="w-full flex items-center justify-between">
          <h2 className='text-black text-xl font-semibold'>Invoices</h2>
          <Button color="primary" startContent={<PlusIcon />} onPress={() => router.push('/newInvoice')}>Add new invoice</Button>
        </div>
        <div className='space-x-5 flex flex-row w-full justify-center'>
          <HomeCards icon="fi-rr-alarm-exclamation" color="#DFE3C7" title="Overdue amount" text="1489.45 RON" />
          <HomeCards icon="fi-rs-sack-dollar" color="#e2d5f3" title="Unpaid totals" text="2500.98 RON" />
          <HomeCards icon="fi-rr-seller" color="#f0e6e6" title="The vendor with the most invoices" text="Enel" />
          <HomeCards icon="fi-rr-payroll-calendar" color="#dce6f7" title="The month with the most expenses" text="January" />
          <SingleHomeCard />
        </div>
        <div className=" p-4 rounded-2xl border-2 border-neutral-100">
          <TableContent />
        </div>
      </div>
    </div>
  )
}