# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 13:08:40 2020

@author: solis
"""

from time import time
import traceback
import littleLogging as logging
from xmlodf import Table_id, Xmlodf

# =============== paramters to fill in ========================
input_file = r'H:\PPHH\2022_27\anejo3_anexos\Anexo_V_Fichas_UDAs_wlxml.xml'
output_file = r'H:\PPHH\2022_27\anejo3_anexos\out\Anexo_V_Fichas_UDAs.csv'

tables_id = [Table_id('superficies',
                      ['uda', 'nombre', 'horizonte', 'superficie', 'bruta'],
                      [1, 2])
             , ]
# =============================================================

def main():
    try:
        startTime = time()

        fi = Xmlodf(input_file, output_file, tables_id)
        fi.extract_tables_using_headers()

    except ValueError:
        msg = traceback.format_exc()
        logging.append(msg)
    except Exception:
        msg = traceback.format_exc()
        logging.append(msg)
    finally:
        logging.dump()
        xtime = time() - startTime
        print(f'Elapsed time {xtime:0.1f} s')


if __name__ == "__main__":
    main()





