--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: feature; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.feature AS
 SELECT q1.user_id,
    q1.plan_id,
    q1.customer_remaining,
    q2.vendor_remaining,
    q3.invoice_remaining,
    q4.bill_remaining,
    q5.bank_remaining,
    q6.cn_remaining,
    q7.dc_remaining,
    q8.dn_remaining,
    q9.doc_remaining,
    q10.estimates_remaining,
    q11.expense_remaining,
    q12.journal_remaining,
    q13.pm_remaining,
    q14.pr_remaining,
    q15.so_remaining,
    q16.statement_remaining,
    q18.po_remaining,
    ((q17.user_roles - q19.user_count) + 1) AS user_remaining,
    q17.items,
    q17.coas,
    q17.profit_loss,
    q17.balance_sheet,
    q17.invoice_details,
    q17.pr_details,
    q17.bill_details,
    q17.pm_details,
    q17.sales_gst,
    q17.purchase_gst,
    q17.gstr_3b,
    q17.gstr_2b,
    q17.gstr_2a,
    q17.inventory,
    q17.inventory_valuation,
    q17.day_book,
    q17.cash_book,
    q17.bank_book,
    q17.webapp,
    q17.backup,
    q17.purchase_orders,
    q17.user_roles,
    q17.company_branches,
    q20.branch_remaining,
    q17.tally,
    q21.filing_remaining,
    q17.full_inventory,
    q17.audit
   FROM ((((((((((((((((((((( SELECT customer_count.user_id,
            customer_count.plan_id,
            customer_count.customers,
            customer_count.customer_count,
            customer_count.customer_remaining
           FROM public.customer_count
          WHERE (customer_count.user_id IS NOT NULL)) q1
     LEFT JOIN ( SELECT vendor_count.user_id,
            vendor_count.vendors,
            vendor_count.vendor_count,
            vendor_count.vendor_remaining
           FROM public.vendor_count
          WHERE (vendor_count.user_id IS NOT NULL)) q2 ON ((q1.user_id = q2.user_id)))
     LEFT JOIN ( SELECT invoice_count.user_id,
            invoice_count.invoices,
            invoice_count.invoice_count,
            invoice_count.invoice_remaining
           FROM public.invoice_count
          WHERE (invoice_count.user_id IS NOT NULL)) q3 ON ((q1.user_id = q3.user_id)))
     LEFT JOIN ( SELECT bill_count.user_id,
            bill_count.bills,
            bill_count.bill_count,
            bill_count.bill_remaining
           FROM public.bill_count
          WHERE (bill_count.user_id IS NOT NULL)) q4 ON ((q1.user_id = q4.user_id)))
     LEFT JOIN ( SELECT bank_count.user_id,
            bank_count.banks,
            bank_count.bank_count,
            bank_count.bank_remaining
           FROM public.bank_count
          WHERE (bank_count.user_id IS NOT NULL)) q5 ON ((q1.user_id = q5.user_id)))
     LEFT JOIN ( SELECT cn_count.user_id,
            cn_count.credit_notes,
            cn_count.cn_count,
            cn_count.cn_remaining
           FROM public.cn_count
          WHERE (cn_count.user_id IS NOT NULL)) q6 ON ((q1.user_id = q6.user_id)))
     LEFT JOIN ( SELECT dc_count.user_id,
            dc_count.delivery_challans,
            dc_count.dc_count,
            dc_count.dc_remaining
           FROM public.dc_count
          WHERE (dc_count.user_id IS NOT NULL)) q7 ON ((q1.user_id = q7.user_id)))
     LEFT JOIN ( SELECT dn_count.user_id,
            dn_count.debit_notes,
            dn_count.dn_count,
            dn_count.dn_remaining
           FROM public.dn_count
          WHERE (dn_count.user_id IS NOT NULL)) q8 ON ((q1.user_id = q8.user_id)))
     LEFT JOIN ( SELECT doc_count.user_id,
            doc_count.scanner,
            doc_count.doc_count,
            doc_count.doc_remaining
           FROM public.doc_count
          WHERE (doc_count.user_id IS NOT NULL)) q9 ON ((q1.user_id = q9.user_id)))
     LEFT JOIN ( SELECT estimate_count.user_id,
            estimate_count.estimates,
            estimate_count.estimate_count,
            estimate_count.estimates_remaining
           FROM public.estimate_count
          WHERE (estimate_count.user_id IS NOT NULL)) q10 ON ((q1.user_id = q10.user_id)))
     LEFT JOIN ( SELECT expense_count.user_id,
            expense_count.expenses,
            expense_count.expense_count,
            expense_count.expense_remaining
           FROM public.expense_count
          WHERE (expense_count.user_id IS NOT NULL)) q11 ON ((q1.user_id = q11.user_id)))
     LEFT JOIN ( SELECT journal_count.user_id,
            journal_count.journals,
            journal_count.journal_count,
            journal_count.journal_remaining
           FROM public.journal_count
          WHERE (journal_count.user_id IS NOT NULL)) q12 ON ((q1.user_id = q12.user_id)))
     LEFT JOIN ( SELECT pm_count.user_id,
            pm_count.pms,
            pm_count.pm_count,
            pm_count.pm_remaining
           FROM public.pm_count
          WHERE (pm_count.user_id IS NOT NULL)) q13 ON ((q1.user_id = q13.user_id)))
     LEFT JOIN ( SELECT pr_count.user_id,
            pr_count.prs,
            pr_count.pr_count,
            pr_count.pr_remaining
           FROM public.pr_count
          WHERE (pr_count.user_id IS NOT NULL)) q14 ON ((q1.user_id = q14.user_id)))
     LEFT JOIN ( SELECT so_count.user_id,
            so_count.sales_orders,
            so_count.so_count,
            so_count.so_remaining
           FROM public.so_count
          WHERE (so_count.user_id IS NOT NULL)) q15 ON ((q1.user_id = q15.user_id)))
     LEFT JOIN ( SELECT count(*) AS user_count,
            registration_user_sub_users.from_user_id
           FROM public.registration_user_sub_users
          GROUP BY registration_user_sub_users.from_user_id) q19 ON ((q1.user_id = q19.from_user_id)))
     LEFT JOIN ( SELECT statement_count.user_id,
            statement_count.statements,
            statement_count.statement_count,
            statement_count.statement_remaining
           FROM public.statement_count
          WHERE (statement_count.user_id IS NOT NULL)) q16 ON ((q1.user_id = q16.user_id)))
     LEFT JOIN ( SELECT po_count.user_id,
            po_count.purchase_orders,
            po_count.po_count,
            po_count.po_remaining
           FROM public.po_count
          WHERE (po_count.user_id IS NOT NULL)) q18 ON ((q1.user_id = q18.user_id)))
     LEFT JOIN ( SELECT branch_count.user_id,
            branch_count.company_branches,
            branch_count.branch_count,
            branch_count.branch_remaining
           FROM public.branch_count
          WHERE (branch_count.user_id IS NOT NULL)) q20 ON ((q1.user_id = q20.user_id)))
     LEFT JOIN ( SELECT filing_count.user_id,
            filing_count.filing,
            filing_count.filing_count,
            filing_count.filing_remaining
           FROM public.filing_count
          WHERE (filing_count.user_id IS NOT NULL)) q21 ON ((q1.user_id = q21.user_id)))
     LEFT JOIN ( SELECT registration_plan.id,
            registration_plan.name,
            registration_plan.validity,
            registration_plan.billing_cycle,
            registration_plan.price,
            registration_plan.backup,
            registration_plan.balance_sheet,
            registration_plan.bank_book,
            registration_plan.banks,
            registration_plan.bill_details,
            registration_plan.bills,
            registration_plan.cash_book,
            registration_plan.coas,
            registration_plan.credit_notes,
            registration_plan.customers,
            registration_plan.day_book,
            registration_plan.debit_notes,
            registration_plan.delivery_challans,
            registration_plan.estimates,
            registration_plan.expenses,
            registration_plan.gstr_2a,
            registration_plan.gstr_2b,
            registration_plan.gstr_3b,
            registration_plan.inventory,
            registration_plan.inventory_valuation,
            registration_plan.invoice_details,
            registration_plan.invoices,
            registration_plan.items,
            registration_plan.journals,
            registration_plan.no_of_branches,
            registration_plan.pm_details,
            registration_plan.pms,
            registration_plan.pr_details,
            registration_plan.profit_loss,
            registration_plan.prs,
            registration_plan.purchase_gst,
            registration_plan.purchase_orders,
            registration_plan.sales_gst,
            registration_plan.sales_orders,
            registration_plan.scanner,
            registration_plan.statements,
            registration_plan.user_roles,
            registration_plan.vendors,
            registration_plan.webapp,
            registration_plan.user_id,
            registration_plan.company_branches,
            registration_plan.tally,
            registration_plan.filing,
            registration_plan.full_inventory,
            registration_plan.audit
           FROM public.registration_plan) q17 ON ((q1.plan_id = q17.id)));


ALTER VIEW public.feature OWNER TO postgres;

--
-- PostgreSQL database dump complete
--

