'use client';

import Image from 'next/image'

export default function HomeCards({ icon = "fi-rr-alarm-exclamation", color = "#DFE3C7", title = "Overdue amount", text = "1489.45 RON" }) {
    return (
        <div className='rounded-2xl border-2 border-neutral-100 w-full h-48 flex items-center justify-center'>
            <div className="w-full h-full flex flex-col items-center justify-center gap-3">
                <div style={{ backgroundColor: color }} className="rounded-full h-16 w-16 flex items-center justify-center">
                    <i className={`fi ${icon} flex items-center justify-center text-xl`}></i>
                </div>
                <div className='flex items-center flex-col'>
                    <h1 className="text-black text-center">{title}</h1>
                    <p className="text-black text-xl font-medium">{text}</p>
                </div>
            </div>
        </div>
    );
}