import calendar
import os
import smtplib
from datetime import date, timedelta
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi_utilities import repeat_at
from sqlalchemy.ext.asyncio import AsyncSession
import mailtrap as mt
from database import get_db

from services.invoice_service import InvoiceService
from services.user_service import UserService

load_dotenv()

class MailerService:
    smtp_token=os.getenv('SMTP_TOKEN')
    smtp_sender_email=os.getenv('SMTP_SENDER_EMAIL')
    smtp_sender_name=os.getenv('SMTP_SENDER_NAME')
    smtp_company_info_name=os.getenv('SMTP_COMPANY_INFO_NAME')
    smtp_company_info_address=os.getenv('SMTP_COMPANY_INFO_ADDRESS')
    smtp_company_info_city=os.getenv('SMTP_COMPANY_INFO_CITY')
    smtp_company_info_zip_code=os.getenv('SMTP_COMPANY_INFO_ZIP_CODE')
    smtp_company_info_country=os.getenv('SMTP_COMPANY_INFO_COUNTRY')
    smtp_demo_recipient_email=os.getenv('SMTP_DEMO_RECIPIENT_EMAIL')

    smtp_due_this_week_template_uuid=os.getenv('SMTP_DUE_THIS_WEEK_TEMPLATE_UUID')
    smtp_due_today_template_uuid=os.getenv('SMTP_DUE_TODAY_TEMPLATE_UUID')
    smtp_overdue_template_uuid=os.getenv('SMTP_OVERDUE_TEMPLATE_UUID')
    smtp_monthly_report_template_uuid=os.getenv('SMTP_MONTHLY_REPORT_TEMPLATE_UUID')

    @staticmethod
    def create_email_from_template(type, user, vendor=None, amount=None, report=None):
        smtp_template_uuid = None
        smtp_template_variables = {
                "company_info_name": MailerService.smtp_company_info_name,
                "company_info_address": MailerService.smtp_company_info_address,
                "company_info_city": MailerService.smtp_company_info_city,
                "company_info_zip_code": MailerService.smtp_company_info_zip_code,
                "company_info_country": MailerService.smtp_company_info_country,
                "vendor": vendor,
                "amount": amount,
                "vendors": report
            }

        if type == 1:
            smtp_template_uuid = MailerService.smtp_due_this_week_template_uuid
        elif type == 2:
            smtp_template_uuid = MailerService.smtp_due_today_template_uuid
        elif type == 3:
            smtp_template_uuid = MailerService.smtp_overdue_template_uuid
        elif type == 4:
            smtp_template_uuid = MailerService.smtp_monthly_report_template_uuid
            # smtp_template_variables["vendors"] = report


        mail = mt.MailFromTemplate(
            sender=mt.Address(email=MailerService.smtp_sender_email, name=MailerService.smtp_sender_name),
            to=[mt.Address(email=user.email)],
            template_uuid=smtp_template_uuid,
            template_variables= smtp_template_variables
        )

        return mail


    @staticmethod
    async def send_reminders():
        '''
        Send a reminder to the user
        '''
        async for db in get_db():
            invoices = await InvoiceService.get_unpaid_by_due_date_range(date.today() + timedelta(days=1), date.today() + timedelta(days=7), db)

            for invoice in invoices:
                user = await UserService.get_by_id(invoice.user_id, db)

                if (user.email == MailerService.smtp_demo_recipient_email): # this is for demo purposes and should be removed once email sending domain is acquired
                    mail = MailerService.create_email_from_template(1, user, vendor=invoice.vendor, amount=invoice.amount)
                    client = mt.MailtrapClient(token=MailerService.smtp_token)
                    client.send(mail)

            invoices = await InvoiceService.get_unpaid_by_due_date(date.today().strftime('%Y-%m-%d'), db)

            for invoice in invoices:
                user = await UserService.get_by_id(invoice.user_id, db)

                if (user.email == MailerService.smtp_demo_recipient_email): # this is for demo purposes and should be removed once email sending domain is acquired
                    mail = MailerService.create_email_from_template(2, user, vendor=invoice.vendor, amount=invoice.amount)
                    client = mt.MailtrapClient(token=MailerService.smtp_token)
                    client.send(mail)

            invoices = await InvoiceService.get_all_unpaid_overdue(db)

            for invoice in invoices:
                user = await UserService.get_by_id(invoice.user_id, db)

                if (user.email == MailerService.smtp_demo_recipient_email): # this is for demo purposes and should be removed once email sending domain is acquired
                    mail = MailerService.create_email_from_template(3, user, vendor=invoice.vendor, amount=invoice.amount)
                    client = mt.MailtrapClient(token=MailerService.smtp_token)
                    client.send(mail)
                
            
            today = date.today()
            first_day = today.replace(day=1)
            last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
            first_day_str = first_day.strftime('%Y-%m-%d')
            last_day_str = last_day.strftime('%Y-%m-%d')

            if True:
                users = await UserService.get_all(db)

                for user in users:
                    report_data = await InvoiceService.get_total_by_vendor_in_date_range(first_day_str, last_day_str, db, user)

                    report = [{"vendor_name": name, "amount": float(amount)} for name, amount in report_data]

                    if(user.email == MailerService.smtp_demo_recipient_email):
                        mail = MailerService.create_email_from_template(4, user, report=report)
                        client = mt.MailtrapClient(token=MailerService.smtp_token)
                        client.send(mail)

            break
