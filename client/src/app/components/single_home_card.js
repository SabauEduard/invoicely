'use client';

import Image from 'next/image'




export default function SingleHomeCard(props) {
    return (
        <div className='rounded-2xl border-2 items-center flex bg-[#f2f7f8] space-x-5 border-gray-100 w-full h-48'>
            <Image
                src="/payment_sticker.png"
                width={150}
                height={150}
                alt="Payment Sticker"
                className='ml-2'
            />
            <div>
                <div className='flex flex-row items-baseline space-x-2'>
                    {
                        props.totalInvoices > 9 ? (
                            <p className='text-black text-3xl font-bold'>{props.totalInvoices}</p>
                        ) : (
                            <p className='text-black text-3xl font-bold'>0{props.totalInvoices}</p>
                        )
                    }
                    <p className='text-black font-bold'>invoices</p>
                </div>
                <div>
                    <p className='text-gray-400 font-medium'>Number of total stored</p>
                </div>
            </div>
        </div>
    );
}