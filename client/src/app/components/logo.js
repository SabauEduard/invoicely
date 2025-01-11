'use client';

import Image from 'next/image'

export default function Logo() {
    return (
        <div className="flex flex-row items-center space-x-2">
            <Image
                src="/invoice2.png"
                width={40}
                height={40}
                alt="Logo Image"
            />
            <h1 className='text-black text-2xl font-[500]'>Invoicely</h1>
        </div>
    );
}