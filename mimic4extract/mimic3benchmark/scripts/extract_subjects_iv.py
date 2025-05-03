from __future__ import absolute_import
from __future__ import print_function

import argparse
import yaml

from mimic3benchmark.mimic3csv import *
from mimic3benchmark.preprocessing import add_hcup_ccs_2015_groups, make_phenotype_label_matrix
from mimic3benchmark.util import dataframe_from_csv

parser = argparse.ArgumentParser(description='Extract per-subject data from MIMIC-III CSV files.')
parser.add_argument('mimic3_path', type=str, help='Directory containing MIMIC-III CSV files.')
parser.add_argument('output_path', type=str, help='Directory where per-subject data should be written.')
parser.add_argument('--filter_subject_id_file', type=str, help='CSV file containing list of subject_ids to keep.')
parser.add_argument('--event_tables', '-e', type=str, nargs='+', help='Tables from which to read events.',
                    default=['OUTPUTEVENTS', 'CHARTEVENTS', 'LABEVENTS'])
parser.add_argument('--phenotype_definitions', '-p', type=str,
                    default=os.path.join(os.path.dirname(__file__), '../resources/icd_9_10_definitions_2.yaml'),
                    help='YAML file with phenotype definitions.')
# parser.add_argument('--itemids_file', '-i', type=str,default=os.path.join(os.path.dirname(__file__),'../resources/itemid_to_variable_map.csv'),
#                     help='CSV containing list of ITEMIDs to keep.')
parser.add_argument('--itemids_file', '-i', type=str, default="/data/wolf6245/src/mm_study/data/f_modelling/01_input/event_names_to_use.xlsx")
parser.add_argument('--verbose', '-v', dest='verbose', action='store_true', help='Verbosity in output')
parser.add_argument('--quiet', '-q', dest='verbose', action='store_false', help='Suspend printing of details')
parser.set_defaults(verbose=True)
parser.add_argument('--test', action='store_true', help='TEST MODE: process only 1000 subjects, 1000000 events.')
args, _ = parser.parse_known_args()

try:
    os.makedirs(args.output_path)
except:
    pass

print("Starting...")
print("Reading patients, admissions, icustays tables...")
patients = read_patients_table(f'{args.mimic3_path}/hosp/patients.csv.gz')
admits = read_admissions_table(f'{args.mimic3_path}/hosp/admissions.csv.gz')
stays = read_icustays_table(f'{args.mimic3_path}/icu/icustays.csv.gz')

if args.verbose:
    print('START:\n\tstay_ids: {}\n\thadm_ids: {}\n\tsubject_ids: {}'.format(stays.stay_id.unique().shape[0],
          stays.hadm_id.unique().shape[0], stays.subject_id.unique().shape[0]))

stays = remove_icustays_with_transfers(stays)

if args.verbose:
    print('REMOVE ICU TRANSFERS:\n\tstay_ids: {}\n\thadm_ids: {}\n\tsubject_ids: {}'.format(stays.stay_id.unique().shape[0],
          stays.hadm_id.unique().shape[0], stays.subject_id.unique().shape[0]))

stays = merge_on_subject_admission(stays, admits)
stays = merge_on_subject(stays, patients)
stays = filter_admissions_on_nb_icustays(stays)

if args.verbose:
    print('REMOVE MULTIPLE STAYS PER ADMIT:\n\tstay_ids: {}\n\thadm_ids: {}\n\tsubject_ids: {}'.format(stays.stay_id.unique().shape[0],
          stays.hadm_id.unique().shape[0], stays.subject_id.unique().shape[0]))


stays = add_age_to_icustays(stays)
stays = add_inunit_mortality_to_icustays(stays)
stays = add_inhospital_mortality_to_icustays(stays)
stays = filter_icustays_on_age(stays)

if args.verbose:
    print('REMOVE PATIENTS AGE < 18:\n\tstay_ids: {}\n\thadm_ids: {}\n\tsubject_ids: {}'.format(stays.stay_id.unique().shape[0],
          stays.hadm_id.unique().shape[0], stays.subject_id.unique().shape[0]))


# Filter stays to only those we want
if args.filter_subject_id_file:
    filter_df = pd.read_parquet(args.filter_subject_id_file)
    subject_ids_to_use = filter_df.subject_id.unique()
    old_stays_len = stays.shape[0]
    stays = stays[stays.subject_id.isin(subject_ids_to_use)]
    if args.verbose:
        print('Filtered for fusion:\n\tstay_ids: {}\n\thadm_ids: {}\n\tsubject_ids: {}'.format(stays.stay_id.unique().shape[0],
          stays.hadm_id.unique().shape[0], stays.subject_id.unique().shape[0]))
        #print(stays.head(2))


stays.to_csv(os.path.join(args.output_path, 'all_stays.csv'), index=False)
if args.verbose:
    print("Stored stays, reading diagnoses...")
diagnoses = read_icd_diagnoses_table(f'{args.mimic3_path}/hosp')
if args.verbose:
    print('Diagnoses shape:', diagnoses.shape)
diagnoses = filter_diagnoses_on_stays(diagnoses, stays)
diagnoses.to_csv(os.path.join(args.output_path, 'all_diagnoses.csv'), index=False)
if args.verbose:
    print('Diagnoses shape after filtering:', diagnoses.shape)
    print("Count icd codes")

count_icd_codes(diagnoses, output_path=os.path.join(args.output_path, 'diagnosis_counts.csv'))

if args.verbose:
    print('Adding HCUP CCS 2015 groups to diagnoses...')

phenotypes = add_hcup_ccs_2015_groups(diagnoses, yaml.load(open(f'{args.phenotype_definitions}', 'r')))

if args.verbose:
    print('Adding phenotype labels to stays...')

make_phenotype_label_matrix(phenotypes, stays).to_csv(os.path.join(args.output_path, 'phenotype_labels.csv'),
                                                      index=False, quoting=csv.QUOTE_NONNUMERIC)

if args.test:
    if args.verbose:
        print('TEST MODE: using only 1000 patients')
    pat_idx = np.random.choice(patients.shape[0], size=1000)
    patients = patients.iloc[pat_idx]
    stays = stays.merge(patients[['subject_id']], left_on='subject_id', right_on='subject_id')
    args.event_tables = [args.event_tables[0]]
    print('Using only', stays.shape[0], 'stays and only', args.event_tables[0], 'table')

if args.verbose:
    print("Break up stays")
subjects = stays.subject_id.unique()
break_up_stays_by_subject(stays, args.output_path, subjects=subjects)
break_up_diagnoses_by_subject(phenotypes, args.output_path, subjects=subjects)
itemids_file = pd.read_excel(args.itemids_file)
def is_numeric(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
# items_to_keep = set([int(itemid) for itemid in dataframe_from_csv(args.itemids_file)['ITEMID'].unique()]) if args.itemids_file else None
items_to_keep = set([int(itemid) for itemid in itemids_file.event_name.unique() if is_numeric(itemid)]) if args.itemids_file else None
print(f"items_to_keep: {len(items_to_keep)}, example: {list(items_to_keep)[:5]}")

if args.verbose:
    print('Reading events tables and breaking up by subject...')

for table in args.event_tables:
    read_events_table_and_break_up_by_subject(f'{args.mimic3_path}', table, args.output_path, items_to_keep=items_to_keep,
                                              subjects_to_keep=subjects)

print("DONE")
