# *****************************************************************************
# Copyright (c) 2019, Intel Corporation All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# *****************************************************************************


import sdc

from .common import Implementation as Impl
from .data_generator import DataGenerator, FloatSeriesGenerator


class Quantile():
    params = [[0.5],
              ['linear', 'nearest', 'lower', 'higher', 'midpoint'],
              ['float', 'int', 'uint'],
              [Impl.interpreted_python.value, Impl.compiled_python.value]]
    pparam_names = ['quantile', 'interpolation', 'dtype', 'implementation']

    def setup(self, quantile, interpolation, dtype, implementation):
        N = 10 ** 7
        data_generator = DataGenerator()
        data = {
            'int': data_generator.make_int_series(N, repeat=5),
            'uint': data_generator.make_uint_series(N, repeat=5),
            'float': data_generator.make_float_series(N, repeat=5),
        }
        self.idx = data[dtype]

    @staticmethod
    @sdc.jit
    def _quantile(idx, quantile, interpolation):
        return idx.quantile(quantile, interpolation=interpolation)

    def time_quantile(self, quantile, interpolation, dtype, implementation):
        if implementation == Impl.compiled_python.value:
            return self._quantile(self.idx, quantile, interpolation)
        if implementation == Impl.interpreted_python.value:
            return self.idx.quantile(quantile, interpolation)


class Absolute:
    params = [
        [3 * 10 ** 8 + 513],
        [Impl.interpreted_python.value, Impl.compiled_python.value]
    ]
    param_names = ['size', 'implementation']

    def setup(self, size, implementation):
        self.series = FloatSeriesGenerator(size=size).generate()

    @staticmethod
    @sdc.jit
    def _abs(series):
        return series.abs()

    def time_abs(self, size, implementation):
        """Time both interpreted and compiled Series.abs"""
        if implementation == Impl.compiled_python.value:
            return self._abs(self.series)
        if implementation == Impl.interpreted_python.value:
            return self.series.abs()


class ValueCounts:
    params = [
        [5 * 10 ** 6 + 513],
        [Impl.interpreted_python.value, Impl.compiled_python.value]
    ]
    param_names = ['size', 'implementation']

    def setup(self, size, implementation):
        self.series = FloatSeriesGenerator(size).generate()

    @staticmethod
    @sdc.jit
    def _value_counts(series):
        return series.value_counts()

    def time_value_counts(self, size, implementation):
        """Time both interpreted and compiled Series.value_counts"""
        if implementation == Impl.compiled_python.value:
            return self._value_counts(self.series)
        if implementation == Impl.interpreted_python.value:
            return self.series.value_counts()


class MinMax:
    params = [
        [25 * 10 ** 7 + 513],
        [Impl.interpreted_python.value, Impl.compiled_python.value]
    ]
    param_names = ['size', 'implementation']

    def setup(self, size, implementation):
        self.series = FloatSeriesGenerator(size=size).generate()

    @staticmethod
    @sdc.jit
    def _min(series):
        return series.min()

    def time_min(self, size, implementation):
        """Time both interpreted and compiled Series.min"""
        if implementation == Impl.compiled_python.value:
            return self._min(self.series)
        if implementation == Impl.interpreted_python.value:
            return self.series.min()

    @staticmethod
    @sdc.jit
    def _max(series):
        return series.max()

    def time_max(self, size, implementation):
        """Time both interpreted and compiled Series.max"""
        if implementation == Impl.compiled_python.value:
            return self._max(self.series)
        if implementation == Impl.interpreted_python.value:
            return self.series.max()


class Correlation:
    params = [
        [10 ** 8 + 513],
        [Impl.interpreted_python.value, Impl.compiled_python.value]
    ]
    param_names = ['size', 'implementation']

    def setup(self, size, implementation):
        self.series = FloatSeriesGenerator(size).generate()
        self.series2 = FloatSeriesGenerator(size).generate()

    @staticmethod
    @sdc.jit
    def _cov(series, series2):
        return series.cov(series2)

    def time_cov(self, size, implementation):
        """Time both interpreted and compiled Series.cov"""
        if implementation == Impl.compiled_python.value:
            return self._cov(self.series, self.series2)
        if implementation == Impl.interpreted_python.value:
            return self.series.cov(self.series2)

    @staticmethod
    @sdc.jit
    def _corr(series, series2):
        return series.corr(series2)

    def time_corr(self, size, implementation):
        """Time both interpreted and compiled Series.cov"""
        if implementation == Impl.compiled_python.value:
            return self._corr(self.series, self.series2)
        if implementation == Impl.interpreted_python.value:
            return self.series.corr(self.series2)


class Sum:
    params = [
        [10 ** 8 + 513],
        [Impl.interpreted_python.value, Impl.compiled_python.value]
    ]
    param_names = ['size', 'implementation']

    def setup(self, size, implementation):
        self.series = FloatSeriesGenerator(size=size).generate()

    @staticmethod
    @sdc.jit
    def _sum(series):
        return series.sum()

    def time_sum(self, size, implementation):
        """Time both interpreted and compiled Series.sum"""
        if implementation == Impl.compiled_python.value:
            return self._sum(self.series)
        if implementation == Impl.interpreted_python.value:
            return self.series.sum()


class Count:
    params = [
        [5 * 10 ** 8 + 513],
        [Impl.interpreted_python.value, Impl.compiled_python.value]
    ]
    param_names = ['size', 'implementation']

    def setup(self, size, implementation):
        self.series = FloatSeriesGenerator(size).generate()

    @staticmethod
    @sdc.jit
    def _count(series):
        return series.count()

    def time_count(self, size, implementation):
        """Time both interpreted and compiled Series.count"""
        if implementation == Impl.compiled_python.value:
            return self._count(self.series)
        if implementation == Impl.interpreted_python.value:
            return self.series.count()


class Nlargest:
    params = [
        [5 * 10 ** 7 + 513],
        [Impl.interpreted_python.value, Impl.compiled_python.value]
    ]
    param_names = ['size', 'implementation']

    def setup(self, size, implementation):
        self.series = FloatSeriesGenerator(size).generate()

    @staticmethod
    @sdc.jit
    def _nlargest(series):
        return series.nlargest()

    def time_nlargest(self, size, implementation):
        if implementation == Impl.compiled_python.value:
            return self._nlargest(self.series)
        if implementation == Impl.interpreted_python.value:
            return self.series.nlargest()


class Nsmallest:
    params = [
        [8 * 10 ** 7 + 513],
        [Impl.interpreted_python.value, Impl.compiled_python.value]
    ]
    param_names = ['size', 'implementation']

    def setup(self, size, implementation):
        self.series = FloatSeriesGenerator(size).generate()

    @staticmethod
    @sdc.jit
    def _nsmallest(series):
        return series.nsmallest()

    def time_nsmallest(self, size, implementation):
        if implementation == Impl.compiled_python.value:
            return self._nsmallest(self.series)
        if implementation == Impl.interpreted_python.value:
            return self.series.nsmallest()


class Var:
    params = [
        [2 * 10 ** 8 + 513],
        [Impl.interpreted_python.value, Impl.compiled_python.value]
    ]
    param_names = ['size', 'implementation']

    def setup(self, size, implementation):
        self.series = FloatSeriesGenerator(size).generate()

    @staticmethod
    @sdc.jit
    def _var(series):
        return series.var()

    def time_var(self, size, implementation):
        if implementation == Impl.compiled_python.value:
            return self._var(self.series)
        if implementation == Impl.interpreted_python.value:
            return self.series.var()


class Mean:
    params = [
        [3 * 10 ** 8 + 513],
        [Impl.interpreted_python.value, Impl.compiled_python.value]
    ]
    param_names = ['size', 'implementation']

    def setup(self, size, implementation):
        self.series = FloatSeriesGenerator(size).generate()

    @staticmethod
    @sdc.jit
    def _mean(series):
        return series.mean()

    def time_mean(self, size, implementation):
        if implementation == Impl.compiled_python.value:
            return self._mean(self.series)
        if implementation == Impl.interpreted_python.value:
            return self.series.mean()


class Median:
    params = [
        [6 * 10 ** 7 + 513],
        [Impl.interpreted_python.value, Impl.compiled_python.value]
    ]
    param_names = ['size', 'implementation']

    def setup(self, size, implementation):
        self.series = FloatSeriesGenerator(size).generate()

    @staticmethod
    @sdc.jit
    def _median(series):
        return series.median()

    def time_median(self, size, implementation):
        if implementation == Impl.compiled_python.value:
            return self._median(self.series)
        if implementation == Impl.interpreted_python.value:
            return self.series.median()
