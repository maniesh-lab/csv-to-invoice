def get_sender_info():
    return {
        "name": "Manish Pandeya",
        "tagline": "Python Automation & Data Solutions",
        "email": "manishpandeya37@gmail.com",
        "location": "Kathmandu, Nepal",
        "github": "github.com/maniesh-lab",
    }


def get_colors():
    return {
        "primary":      (23, 37, 84),      # deep navy — header background
        "accent":       (59, 130, 246),    # clean blue — highlights and borders
        "light_bg":     (241, 245, 249),   # very light grey — alternating table rows
        "white":        (255, 255, 255),
        "text_dark":    (15, 23, 42),      # near black — body text
        "text_muted":   (100, 116, 139),   # grey — labels and secondary text
        "success":      (34, 197, 94),     # green — total due row accent
    }


def get_fonts():
    return {
        "heading":      {"family": "Helvetica", "style": "B", "size": 22},
        "subheading":   {"family": "Helvetica", "style": "B", "size": 11},
        "label":        {"family": "Helvetica", "style": "B", "size": 9},
        "body":         {"family": "Helvetica", "style": "",  "size": 9},
        "small":        {"family": "Helvetica", "style": "",  "size": 8},
        "total":        {"family": "Helvetica", "style": "B", "size": 11},
        "tagline":      {"family": "Helvetica", "style": "I", "size": 9},
    }


def get_layout():
    return {
        "margin":           15,     # page margin in mm
        "row_height":       8,      # standard table row height
        "header_height":    28,     # top header block height
        "col_service":      95,     # width of service description column
        "col_amount":       35,     # width of amount columns
        "section_gap":      8,      # vertical space between sections
    }