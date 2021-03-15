import gzip
import os
import logging
from lxml import etree
from datetime import date, datetime


def initiate_logfile(log_file_name, log_path):

    current_date_time = datetime.now()
    logname = log_file_name + "_{}.log".format(
        current_date_time.strftime("%d%m%Y_%H%M%S")
    )

    logging.basicConfig(
        filename=log_path + "\\" + logname,
        format="%(asctime)s - %(levelname)s : %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S GMT%z",
        encoding="utf-8",
        level=logging.DEBUG,
    )


def validate_lrt_B(dir_lrt):
    list_in = os.listdir(path=dir_lrt)
    list_out = []
    for lrt in list_in:
        if lrt.startswith("B") and lrt.endswith(".gz"):
            list_out.append(dir_lrt + "\\" + lrt)
            logging.info("Successfully obtained LRT: {}".format(lrt))
    logging.info("Total LRTs obtained: {}\n".format(len(list_out)))
    return list_out


def validate_lrt_B_with_logger(dir_lrt, logger_name):
    list_in = os.listdir(path=dir_lrt)
    list_out = []
    for lrt in list_in:
        if lrt.startswith("B") and lrt.endswith(".gz"):
            list_out.append(lrt)
            logger_name.info("Successfully obtained LRT: {}".format(lrt))
    logger_name.info("Total LRTs obtained: {}\n".format(len(list_out)))
    return list_out


def validate_lrt_all(dir_lrt):
    list_in = os.listdir(path=dir_lrt)
    list_out = []
    for lrt in list_in:
        if lrt.endswith(".gz"):
            list_out.append(dir_lrt + "\\" + lrt)
            logging.info("Successfully obtained LRT: {}".format(lrt))
    logging.info("Total LRTs obtained: {}\n".format(len(list_out)))
    return list_out


def gunzip_lrt(input_file):
    output_file = input_file.rstrip(".gz")
    with gzip.open(input_file, "rt") as fin:
        with open(output_file, "w") as fout:
            fout.write(fin.read())
    logging.info(
        "Successfully gunzip file {} to file {}".format(input_file, output_file)
    )
    os.remove(input_file)
    return output_file


def gunzip_lrt_with_logger(input_file, logger_name):
    output_file = input_file.rstrip(".gz")
    with gzip.open(input_file, "rt") as fin:
        with open(output_file, "w") as fout:
            fout.write(fin.read())
    logger_name.info(
        "Successfully gunzip file {} to file {}".format(input_file, output_file)
    )
    os.remove(input_file)
    return output_file


def gzip_lrt(input_file):
    output_file = input_file + ".gz"
    with open(input_file, "r") as fin:
        with gzip.open(output_file, "wt") as fout:
            fout.write(fin.read())
    logging.info("Successfully gzip file {} to file {}".format(input_file, output_file))

    os.remove(input_file)
    return output_file


def gzip_lrt_with_logger(input_file, logger_name):
    output_file = input_file + ".gz"
    with open(input_file, "r") as fin:
        with gzip.open(output_file, "wt") as fout:
            fout.write(fin.read())
    logger_name.info(
        "Successfully gzip file {} to file {}".format(input_file, output_file)
    )

    os.remove(input_file)
    return output_file


def modify_lrt_sag(file_xml, tcontext, from_sag, to_sag):
    tree = etree.parse(file_xml)
    root = tree.getroot()
    n = 0

    for element in root.iter("next"):
        if to_sag not in element.text:
            if tcontext in element.text:
                element.text = element.text.replace(from_sag, to_sag)
                n += 1

    logging.info("In total has been modified {} entries".format(n))

    xml_data = etree.tostring(
        tree, pretty_print=True, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    with open(file_xml, "wb") as f:
        f.write(xml_data)
    logging.info("Successfully modified LRT {}".format(file_xml))


def modify_lrt_sag_with_logger(file_xml, tcontext, from_sag, to_sag, logger_name):
    tree = etree.parse(file_xml)
    root = tree.getroot()
    n = 0

    for element in root.iter("next"):
        if to_sag not in element.text:
            if tcontext in element.text:
                element.text = element.text.replace(from_sag, to_sag)
                n += 1

    logger_name.info("In total has been modified {} entries".format(n))

    xml_data = etree.tostring(
        tree, pretty_print=True, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    with open(file_xml, "wb") as f:
        f.write(xml_data)
    logger_name.info("Successfully modified LRT {}".format(file_xml))


def validate_lrt_format(lrt):
    try:
        xmlschema = etree.XMLSchema(file="validate.xsd")
        tree = etree.parse(lrt)
    except etree.XMLSyntaxError as e:
        e_str = str(e)
        print(
            "The file {} has syntax errors, first error found is: {}".format(
                lrt, e_str.split("(")[0]
            )
        )
        logging.critical(
            "The file {} has syntax errors, first error found is: {}".format(
                lrt, e_str.split("(")[0]
            )
        )
    else:
        if xmlschema.validate(tree):
            print("The file {} is well formed and valid".format(lrt))
            logging.info("The file {} is well formed and valid".format(lrt))
            os.remove(lrt)
        else:
            try:
                xmlschema.assertValid(tree)
            except etree.DocumentInvalid as e:
                print("The file {} is well formed but invalid: {}".format(lrt, e))
                logging.error(
                    "The file {} is well formed but invalid: {}".format(lrt, e)
                )


def remove_file_by_extension(dir, exten):
    for f in os.listdir(dir):
        if f.endswith(exten):
            os.remove(os.path.join(dir, f))