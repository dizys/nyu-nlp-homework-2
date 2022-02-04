from datetime import datetime
import os
from os import path
from pathlib import Path
from collections import Counter
import json

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

PROJECT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
DATA_DIR = path.join(PROJECT_DIR, 'data')
ALL_OANC_CORPUS_PATH = path.join(DATA_DIR, 'all-OANC.txt')
TEST_DOLLAR_PHONE_CORPUS_PATH = path.join(DATA_DIR, 'test_dollar_phone_corpus.txt')
TEST_DOLLAR_REFERENCE_PATH = path.join(DATA_DIR, 'test_dollar_reference.txt')
TEST_PHONE_REFERENCE_PATH = path.join(DATA_DIR, 'test_phone_reference.txt')
SRC_DIR = path.join(PROJECT_DIR, 'src')
DOLLAR_PROGRAM_PATH = path.join(SRC_DIR, 'dollar_program.py')
TELEPHONE_REGEXP_PATH = path.join(SRC_DIR, 'telephone_regexp.py')
OUT_DIR = path.join(PROJECT_DIR, 'out')
ALL_OANC_DOLLAR_PROGRAM_OUT_PATH = path.join(OUT_DIR, 'all-OANC_dollar_program.txt')
ALL_OANC_TELEPHONE_REGEXP_OUT_PATH = path.join(OUT_DIR, 'all-OANC_telephone_regexp.txt')
TEST_DOLLAR_PROGRAM_OUT_PATH = path.join(OUT_DIR, 'test_dollar_program.txt')
TEST_TELEPHONE_REGEXP_OUT_PATH = path.join(OUT_DIR, 'test_telephone_regexp.txt')
EVALUATION_RESULTS_PATH = path.join(OUT_DIR, 'evaluation_results.json')

INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = "derzart@gmail.com"
INFLUX_BUCKET = "nlp-homework"

def run_extraction_program(program_path, corpus_path, out_path):
    os.system(f'python3 {program_path} {corpus_path} > {out_path}')

def get_output_statistics(output_path):
    with open(output_path, 'r') as f:
        output_lines = f.readlines()

    output_counter = Counter([line.strip() for line in output_lines if line.strip() != ''])

    return {
        "total_count": sum(output_counter.values()),
        "items": len(output_counter.keys()),
    }

def evaluate_outputs(reference_path, out_path):
    with open(reference_path, 'r') as f:
        reference_lines = f.readlines()
    with open(out_path, 'r') as f:
        out_lines = f.readlines()

    reference_counter = Counter([line.strip() for line in reference_lines if line.strip() != ''])
    out_counter = Counter([line.strip() for line in out_lines if line.strip() != ''])

    reference_counter[''] = 0
    out_counter[''] = 0

    correct_out_count = 0
    for key, value in out_counter.items():
        if key in reference_counter:
            correct_out_count += min(value, reference_counter[key])

    if len(out_lines) == 0 or len(reference_lines) == 0:
        precision = 0
        recall = 0
    else:
        precision = correct_out_count / len(out_lines)
        recall = correct_out_count / len(reference_lines)

    return {
        "precision": precision,
        "recall": recall,
    }


def report_evaluation_results(evaluation_results):
    if not INFLUX_TOKEN:
        print("No InfluxDB token provided, skipping InfluxDB reporting")
        return
    
    with InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=INFLUX_TOKEN, org=INFLUX_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        point = Point("hw2_evaluation_results")

        point.tag("assignment", "nlp-homework-2")
        for item in evaluation_results.keys():
            for key in evaluation_results[item].keys():
                point.field(f"{item}:{key}", evaluation_results[item][key])
        
        write_api.write(INFLUX_BUCKET, INFLUX_ORG, point)


def main():
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    print('Running dollar program on all OANC corpus...')
    run_extraction_program(DOLLAR_PROGRAM_PATH, ALL_OANC_CORPUS_PATH, ALL_OANC_DOLLAR_PROGRAM_OUT_PATH)
    print('- Done.')

    print('Running telephone regexp on all OANC corpus...')
    run_extraction_program(TELEPHONE_REGEXP_PATH, ALL_OANC_CORPUS_PATH, ALL_OANC_TELEPHONE_REGEXP_OUT_PATH)
    print('- Done.')

    print('Running dollar program on test dollar corpus...')
    run_extraction_program(DOLLAR_PROGRAM_PATH, TEST_DOLLAR_PHONE_CORPUS_PATH, TEST_DOLLAR_PROGRAM_OUT_PATH)
    print('- Done.')

    print('Running telephone regexp on test dollar corpus...')
    run_extraction_program(TELEPHONE_REGEXP_PATH, TEST_DOLLAR_PHONE_CORPUS_PATH, TEST_TELEPHONE_REGEXP_OUT_PATH)
    print('- Done.')

    print('Evaluating output...')
    test_dollar_evaluation = evaluate_outputs(TEST_DOLLAR_REFERENCE_PATH, TEST_DOLLAR_PROGRAM_OUT_PATH)
    test_phone_evaluation = evaluate_outputs(TEST_PHONE_REFERENCE_PATH, TEST_TELEPHONE_REGEXP_OUT_PATH)
    print('- Done.')

    evaluation_results = {
        "all-OANC_dollar_program": get_output_statistics(ALL_OANC_DOLLAR_PROGRAM_OUT_PATH),
        "all-OANC_telephone_regexp": get_output_statistics(ALL_OANC_TELEPHONE_REGEXP_OUT_PATH),
        "test_dollar_program": get_output_statistics(TEST_DOLLAR_PROGRAM_OUT_PATH),
        "test_telephone_regexp": get_output_statistics(TEST_TELEPHONE_REGEXP_OUT_PATH),
        "test_dollar_program_evaluation": test_dollar_evaluation,
        "test_telephone_regexp_evaluation": test_phone_evaluation,
    }

    print('Writing evaluation results to file...')

    with open(EVALUATION_RESULTS_PATH, 'w') as f:
        json.dump(evaluation_results, f, indent=4)
        print(f"- Done. Results written to file: {EVALUATION_RESULTS_PATH}")
    
    print('Evaluation results:')
    print(json.dumps(evaluation_results, indent=4))

    print('Reporting evaluation results to InfluxDB...')
    report_evaluation_results(evaluation_results)
    print('- Done.')


if __name__ == '__main__':
    main()