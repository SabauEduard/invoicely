'use client';

import Logo from './components/logo.js';
import HomeCards from './components/home_cards.js';
import SingleHomeCard from './components/single_home_card.js';
import { Button, Input } from "@nextui-org/react";
import Search from './components/search.js';
import TableContent from './components/tableContent.js';

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
  return (
    <div className='bg-neutral-100 min-h-screen flex flex-col'>
      <div className="flex items-center justify-between w-full h-20 px-6">
        <Logo />
        <i className="text-black fi fi-tr-circle-user text-[32px] flex items-center"></i>
      </div>
      <div
        className="bg-white px-10 py-8 rounded-l-3xl ml-20 mb-10 space-y-8">
        <div className="w-full flex items-center justify-between">
          <h2 className='text-black text-xl font-semibold'>Invoices</h2>
          <Button color="primary" startContent={<PlusIcon />}>Add new invoice</Button>
        </div>
        <div className='space-x-5 flex flex-row w-full justify-center'>
          <HomeCards />
          <HomeCards />
          <HomeCards />
          <HomeCards />
          <SingleHomeCard />
        </div>
        <div className=" p-4 rounded-2xl border-2 border-neutral-100">
          <TableContent />
        </div>
      </div>
    </div>
  )
}