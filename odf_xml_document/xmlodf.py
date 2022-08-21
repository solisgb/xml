# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 14:22:17 2022

@author: solis
"""
from copy import deepcopy
import csv
import xml.etree.ElementTree as ET


class Table_id():
    """
    Table in document
    Each table is divided into other tables within the document that are
    interspersed with other tables with other contents. Each time a table is
    found in the document it must be identified by its first line, which is
    the table header.
    """

    def __init__(self, tid: str, key_names_in_row0: [str],
                 cols_eq_content: [int]):
        """

        Parameters
        ----------
        tid : str
            Unique identifier for tables with the same type of data.
        key_names_in_row0 : [str]
            Words characterizing the table header.
        cols_eq_content : [int]
            In some tables, some columns with the same content are written
            only once. List of columns with this layout (starting with 1).

        Returns
        -------
        None.

        """
        self.tid = tid
        self.key_names_in_row0 = [kn1 for kn1 in key_names_in_row0]
        self.cols_eq_content = deepcopy(cols_eq_content)


class Xmlodf():
    """
    Class to read odf files saved as flat xml odf text document
    """


    def __init__(self, input_file: str, output_file: str,
                 tables_id: [Table_id] ):
        """

        Parameters
        ----------
        input_file : str
            Input file name.
        output_file : str
            Output file name.
        tables_id : [Table_id]
            Tables whose contents are to be extracted and identified as an
            instance of the Table_id class. Tables that are not referenced by
            a Table_id instance will not be extracted.

        Returns
        -------
        None.

        """
        self.fi = input_file
        self.fo = output_file
        self.tid = deepcopy(tables_id)


    def extract_tables_using_headers(self):
        """
        Reads the file self.fi and writes the file self.fo. For the same
        self.fi file, the contents of the output file will vary according
        to the contents of self.tid.

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        None.

        """

        tree = ET.parse(self.fi)
        root = tree.getroot()
        tables = root.findall("./page/body/tab")
        if len(tables) == 0:
            raise ValueError(f'No tables in {self.fi}')
        print(f'number of tables {len(tables)}')

        headers_already_recorded = []
        with open(self.fo, 'w', encoding='utf-8', newline='') as fo:

            writer = csv.writer(fo, delimiter=',')

            for table in tables:
                rows = table.findall("row")
                table_id = None
                for ir, row in enumerate(rows):
                    cells = row.findall("cell")
                    txt_in_cells = ['' for item in range(len(cells))]
                    for i, cell in enumerate(cells):
                        txts = cell.findall("txt")
                        for txt1 in txts:
                            st = ''.join([s.strip() for s in txt1.itertext()])
                            st = self.__clean_cells_text(st)
                            if len(st) > 0:
                                txt_in_cells[i] += st

                    if table_id is None:
                        tid = self.table_id_get(txt_in_cells)
                        if tid is None:
                            continue
                        else:
                            table_id = tid.tid

                        if table_id in headers_already_recorded:
                            continue
                        headers_already_recorded.append(table_id)

                    if ir == 1:
                        prev_contents = [item for item in txt_in_cells]
                    elif ir > 1:
                        for col1 in tid.cols_eq_content:
                            icol1 = col1 - 1
                            if len(txt_in_cells[icol1]) == 0:
                                txt_in_cells[icol1] = prev_contents[icol1]

                    txt_in_cells.insert(0, table_id)
                    writer.writerow(txt_in_cells)


    def table_id_get(self, values: [str]):
        """
        For each table in self.fi it identifies which table it is based on
        the contents of the header, which is compared to the list of words
        in values. If there is no match it returns None.

        Parameters
        ----------
        values : [str]
            List of words that must be present in the header of a table for
            it to be identified.

        Returns
        -------
        tid1 : Table_id or None

        """
        v = [value.lower() for value in values]
        header = ' '.join(v)
        if len(header) == 0:
            return None

        for tid1 in self.tid:
            for kn1 in tid1.key_names_in_row0:
                if kn1 not in header:
                    return None
            return tid1

        return None

    def __clean_cells_text(self, text:str):
        """
        Clears the contents of a word

        Parameters
        ----------
        text : str
            Word to be cleaned.

        Returns
        -------
        str
            cleaned word.

        """
        text = text.strip()
        text = text.replace('\n', '')
        lst = text.split()
        return ' '.join(lst)


