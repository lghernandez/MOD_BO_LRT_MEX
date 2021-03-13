import gzip
import os
import logging
from lxml import etree
from datetime import date, datetime


def create_custom_logger(logger_name, log_path):

    current_date_time = datetime.now()
    logname = logger_name + "_{}.log".format(
        current_date_time.strftime("%d%m%Y_%H%M%S")
    )

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    log_format = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s : %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S GMT%z",
    )
    log_file = os.path.join(log_path, logname)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    return logger, log_file


def validate_lrt_all(dir_lrt, logger_name):
    list_in = os.listdir(path=dir_lrt)
    list_out = []
    for lrt in list_in:
        if lrt.endswith(".gz"):
            list_out.append(dir_lrt + "\\" + lrt)
            logger_name.info("Successfully obtained LRT: {}".format(lrt))
    logger_name.info("Total LRTs obtained: {}\n".format(len(list_out)))
    return list_out


def gunzip_lrt(input_file, logger_name):
    output_file = input_file.rstrip(".gz")
    try:
        with gzip.open(input_file, "rt") as fin:
            with open(output_file, "w") as fout:
                fout.write(fin.read())
        logger_name.info(
            "Successfully gunzip file {} to file {}".format(input_file, output_file)
        )
        os.remove(input_file)
        return output_file
    except gzip.BadGzipFile as e:
        logger_name.critical(
            "The file {} is not in gzip format: {}".format(input_file, e)
        )


def validate_lrt_format(lrt, logger_name):
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
        logger_name.critical(
            "The file {} has syntax errors, first error found is: {}".format(
                lrt, e_str.split("(")[0]
            )
        )
    else:
        if xmlschema.validate(tree):
            print("The file {} is well formed and valid".format(lrt))
            logger_name.info("The file {} is well formed and valid".format(lrt))
            os.remove(lrt)
        else:
            try:
                xmlschema.assertValid(tree)
            except etree.DocumentInvalid as e:
                print("The file {} is well formed but invalid: {}".format(lrt, e))
                logger_name.error(
                    "The file {} is well formed but invalid: {}".format(lrt, e)
                )


def remove_file_by_extension(dir, exten):
    for f in os.listdir(dir):
        if f.endswith(exten):
            os.remove(os.path.join(dir, f))