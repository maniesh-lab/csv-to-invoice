from fpdf import FPDF
from pathlib import Path
from templates import get_sender_info, get_colors, get_fonts, get_layout

def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    layout = get_layout()
    pdf.set_margins(layout["margin"], layout["margin"], layout["margin"])
    pdf.set_auto_page_break(auto=True, margin=layout["margin"])
    return pdf


def add_header(pdf, invoice_number):
    colors  = get_colors()
    fonts   = get_fonts()
    layout  = get_layout()
    sender  = get_sender_info()

    # Navy background bar
    pdf.set_fill_color(*colors["primary"])
    pdf.rect(0, 0, 210, layout["header_height"] + 14, style="F")

    # Your name — top left
    pdf.set_xy(layout["margin"], 8)
    pdf.set_font(fonts["heading"]["family"], fonts["heading"]["style"], fonts["heading"]["size"])
    pdf.set_text_color(*colors["white"])
    pdf.cell(120, 10, sender["name"], ln=0)

    # Invoice label — top right
    pdf.set_font(fonts["subheading"]["family"], fonts["subheading"]["style"], fonts["subheading"]["size"])
    pdf.set_xy(140, 8)
    pdf.cell(55, 10, "INVOICE", align="R", ln=1)

    # Tagline — below name
    pdf.set_xy(layout["margin"], 17)
    pdf.set_font(fonts["tagline"]["family"], fonts["tagline"]["style"], fonts["tagline"]["size"])
    pdf.set_text_color(*colors["accent"])
    pdf.cell(120, 6, sender["tagline"], ln=0)

    # Invoice number — below INVOICE label
    pdf.set_xy(140, 17)
    pdf.set_font(fonts["small"]["family"], fonts["small"]["style"], fonts["small"]["size"])
    pdf.set_text_color(*colors["white"])
    pdf.cell(55, 6, f"#{invoice_number}", align="R", ln=1)

    pdf.ln(layout["section_gap"] + 4)


def add_sender_details(pdf):
    colors  = get_colors()
    fonts   = get_fonts()
    layout  = get_layout()
    sender  = get_sender_info()

    pdf.set_x(layout["margin"])
    pdf.set_font(fonts["label"]["family"], fonts["label"]["style"], fonts["label"]["size"])
    pdf.set_text_color(*colors["text_muted"])
    pdf.cell(0, 6, "FROM", ln=1)

    pdf.set_font(fonts["body"]["family"], fonts["body"]["style"], fonts["body"]["size"])
    pdf.set_text_color(*colors["text_dark"])
    pdf.set_x(layout["margin"])
    pdf.cell(0, 5, sender["email"], ln=1)
    pdf.set_x(layout["margin"])
    pdf.cell(0, 5, sender["github"], ln=1)
    pdf.set_x(layout["margin"])
    pdf.cell(0, 5, sender["location"], ln=1)

    pdf.ln(layout["section_gap"])


def add_client_section(pdf, invoice_data):
    colors  = get_colors()
    fonts   = get_fonts()
    layout  = get_layout()

    # "BILL TO" label
    pdf.set_x(layout["margin"])
    pdf.set_font(fonts["label"]["family"], fonts["label"]["style"], fonts["label"]["size"])
    pdf.set_text_color(*colors["text_muted"])
    pdf.cell(0, 6, "BILL TO", ln=1)

    # Client name
    pdf.set_x(layout["margin"])
    pdf.set_font(fonts["subheading"]["family"], fonts["subheading"]["style"], fonts["subheading"]["size"])
    pdf.set_text_color(*colors["text_dark"])
    pdf.cell(0, 6, invoice_data["client_name"], ln=1)

    # Due date — right aligned
    pdf.set_xy(140, pdf.get_y() - 6)
    pdf.set_font(fonts["label"]["family"], fonts["label"]["style"], fonts["label"]["size"])
    pdf.set_text_color(*colors["text_muted"])
    pdf.cell(55, 5, "DUE DATE", align="R", ln=1)

    pdf.set_xy(140, pdf.get_y())
    pdf.set_font(fonts["body"]["family"], fonts["body"]["style"], fonts["body"]["size"])
    pdf.set_text_color(*colors["text_dark"])
    pdf.cell(55, 5, invoice_data["due_date"], align="R", ln=1)

    pdf.ln(layout["section_gap"])


def add_items_table(pdf, invoice_data):
    colors  = get_colors()
    fonts   = get_fonts()
    layout  = get_layout()

    col_s = layout["col_service"]
    col_a = layout["col_amount"]

    # Table header row
    pdf.set_fill_color(*colors["primary"])
    pdf.set_text_color(*colors["white"])
    pdf.set_font(fonts["label"]["family"], fonts["label"]["style"], fonts["label"]["size"])
    pdf.set_x(layout["margin"])
    pdf.cell(col_s, layout["row_height"] + 2, "DESCRIPTION",    fill=True, border=0)
    pdf.cell(col_a, layout["row_height"] + 2, "RATE",   align="R", fill=True, border=0)
    pdf.cell(col_a, layout["row_height"] + 2, "AMOUNT", align="R", fill=True, border=0, ln=1)

    # Item row
    pdf.set_fill_color(*colors["light_bg"])
    pdf.set_text_color(*colors["text_dark"])
    pdf.set_font(fonts["body"]["family"], fonts["body"]["style"], fonts["body"]["size"])
    pdf.set_x(layout["margin"])
    pdf.cell(col_s, layout["row_height"] + 2, invoice_data["service"],                         fill=True, border=0)
    pdf.cell(col_a, layout["row_height"] + 2, f"${invoice_data['amount']:.2f}", align="R",     fill=True, border=0)
    pdf.cell(col_a, layout["row_height"] + 2, f"${invoice_data['amount']:.2f}", align="R",     fill=True, border=0, ln=1)

    pdf.ln(layout["section_gap"] - 2)


def add_totals_section(pdf, invoice_data):
    colors  = get_colors()
    fonts   = get_fonts()
    layout  = get_layout()

    start_x = 210 - layout["margin"] - (layout["col_amount"] * 2)

    def totals_row(label, value, bold=False, highlight=False):
        if highlight:
            pdf.set_fill_color(*colors["primary"])
            pdf.set_text_color(*colors["white"])
        else:
            pdf.set_fill_color(*colors["white"])
            pdf.set_text_color(*colors["text_dark"])

        style = "B" if bold else ""
        pdf.set_font(fonts["body"]["family"], style, fonts["body"]["size"] if not bold else fonts["total"]["size"])
        pdf.set_x(start_x)
        pdf.cell(layout["col_amount"], layout["row_height"], label, fill=highlight, border=0)
        pdf.cell(layout["col_amount"], layout["row_height"], value, align="R", fill=highlight, border=0, ln=1)

    totals_row("Subtotal",  f"${invoice_data['amount']:.2f}")
    totals_row(f"Tax ({invoice_data['tax_rate']:.0f}%)", f"${invoice_data['tax_amount']:.2f}")
    totals_row("TOTAL DUE", f"${invoice_data['total']:.2f}", bold=True, highlight=True)

    pdf.ln(layout["section_gap"])


def add_footer(pdf):
    colors  = get_colors()
    fonts   = get_fonts()

    pdf.set_y(-25)
    pdf.set_font(fonts["small"]["family"], fonts["small"]["style"], fonts["small"]["size"])
    pdf.set_text_color(*colors["text_muted"])
    pdf.set_x(15)
    pdf.cell(0, 5, "Thank you for your business.", ln=1)
    pdf.set_x(15)
    pdf.cell(0, 5, "Payment via bank transfer or PayPal. Please include the invoice number as reference.", ln=1)


def save_invoice(pdf, client_name, invoice_number):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    clean_name = client_name.replace(" ", "")
    filename = output_dir / f"Invoice_{clean_name}_{invoice_number}.pdf"
    pdf.output(str(filename))
    return filename


def build_invoice(invoice_data, invoice_number):
    pdf = create_pdf()
    add_header(pdf, invoice_number)
    add_sender_details(pdf)
    add_client_section(pdf, invoice_data)
    add_items_table(pdf, invoice_data)
    add_totals_section(pdf, invoice_data)
    add_footer(pdf)
    filename = save_invoice(pdf, invoice_data["client_name"], invoice_number)
    return filename