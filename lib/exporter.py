"""
Exporter backend
"""
import html
import sys

import pdfkit


def view_models_to_html(view_models: list):
    """
    Converts a list of view models into an HTML table

    :param view_models: list
    :return: HTML string
    """
    result = '<table>' \
             '<tr>'
    columns = view_models[0].keys()

    for column in columns:
        result += f'<th>{column}</th>'

    result += '</tr>'

    for row in view_models:
        result += '<tr>'
        for column in columns:
            result += f'<td>{html.escape(row[column])}</td>'
        result += '</tr>'

    result += '</table>'
    return result


def table_to_html(table_model):
    """

    :param table_model:
    :return:
    """
    view_models = []

    recs = table_model.getAllCells()
    colnames = table_model.columnNames
    collabels = table_model.columnlabels

    for row_id in recs.keys():
        view_model = {}
        i = 0
        for cell in recs[row_id]:
            if not cell or cell == 'None':
                cell = ''
            view_model[collabels[colnames[i]]] = cell
            i += 1

        view_models.append(view_model)

    return view_models_to_html(view_models)


def html_to_pdf(html_str: str, filepath: str):
    """
    Uses PDFKit to convert an HTML string into a PDF, given
    a filepath

    :param html_str: HTML string
    :param filepath: File path, preferably from a save as picker
    :return: True on success
    """
    if getattr(sys, 'frozen', False):
        # config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')
        return pdfkit.from_string(html_str, filepath, options={
            'quiet': '',
            'orientation': 'landscape'
        })
    return pdfkit.from_string(html_str, filepath, options={
        'quiet': '',
        'orientation': 'landscape'
    })
