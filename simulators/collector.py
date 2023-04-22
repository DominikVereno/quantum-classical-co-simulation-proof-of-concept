import collections
from datetime import datetime

import pandas as pd
import numpy as np

import mosaik_api


META = {
    'type': 'event-based',
    'models': {
        'Monitor': {
            'public': True,
            'any_inputs': True,
            'params': [],
            'attrs': [],
        },
    },
}


class Collector(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.time = 0

    def init(self, simulator_id, time_resolution, persist_data = False, log_file_suffix = ""):
        self.simulator_id = simulator_id
        self.time_resolution = time_resolution
        
        self.persist_data = persist_data
        self.logfile_suffix = log_file_suffix

        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError('Can only create one instance of Monitor.')

        self.eid = 'Monitor'

        self.data = collections.defaultdict(lambda: collections.defaultdict(dict))
        self.df = pd.DataFrame()

        return [{'eid': self.eid, 'type': model}]

    def step(self, time, inputs, max_advance):
        self.time = time
        data = inputs.get(self.eid, {})
        for attr, values in data.items():
            for src, value in values.items():
                row = {
                    "entity": src,
                    "attr"  : attr,
                    "time"  : time,
                    "value" : value
                } 
                self.df = self.df.append(row, ignore_index=True)

        return None

    def finalize(self):
        self.__reformat_data()

        self.__print_collected_data_to_cli()

        if self.persist_data:
            self.__create_csv_logfile()

    def __reformat_data(self):
        index_tuples = set(zip(list(self.df["entity"]), list(self.df["attr"])))
        index = pd.MultiIndex.from_tuples(index_tuples, names=["entity", "attribute"])

        reformated_df = pd.DataFrame(np.zeros((len(index_tuples), self.time+1)), index=index)
        for _, row in self.df.iterrows():
            reformated_df.loc[row["entity"], row["attr"]][row["time"]] = row["value"]

        self.df = reformated_df

    def __print_collected_data_to_cli(self, value_format="{0:+0.4f}"):
        first_index_length  = longtest_string_length(self.df.index.get_level_values(0))
        second_index_length = longtest_string_length(self.df.index.get_level_values(1))

        for index, row in self.df.iterrows():
            formated_values = [value_format.format(value) for value in row]
            padded_entity = index[0].ljust(first_index_length, " ")
            padded_attr   = index[1].ljust(second_index_length, " ")

            print(f" - {padded_entity} - {padded_attr}: ", end="")
            print_list(formated_values)

    def __create_csv_logfile(self):
        datetime_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.df.to_csv(f"simulation_results/{datetime_string}_{self.logfile_suffix}.csv")

def print_list(value_list):
    print("[", end="")
    print(", ".join(value_list), end="")
    print("]")

def longtest_string_length(value_list):
    return max([len(value) for value in value_list])
