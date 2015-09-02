# -*- coding: utf-8 -*-

#   Copyright (c) 2010-2014, MIT Probabilistic Computing Project
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import bayeslite
import bayeslite.geweke_testing as geweke

def test_geweke_troll():
    with bayeslite.bayesdb_open() as bdb:
        import bayeslite.metamodels.troll_rng as troll
        bayeslite.bayesdb_register_metamodel(bdb, troll.TrollMetamodel())
        kl_est = geweke.geweke_kl(bdb, "troll_rng", [['column', 'numerical']], \
            ['column'], [(1,0)], 2, 2, 2, 2)
        assert kl_est == (2, 0, 0)

def test_geweke_iid_gaussian():
    with bayeslite.bayesdb_open() as bdb:
        import bayeslite.metamodels.iid_gaussian as gauss
        bayeslite.bayesdb_register_metamodel(bdb, gauss.StdNormalMetamodel())
        kl_est = geweke.geweke_kl(bdb, "std_normal", [['column', 'numerical']], \
            ['column'], [(1,0), (2,0)], 2, 2, 2, 2)
        assert kl_est == (2, 0, 0)

def test_geweke_nig_normal():
    with bayeslite.bayesdb_open() as bdb:
        import bayeslite.metamodels.nig_normal as normal
        bayeslite.bayesdb_register_metamodel(bdb, normal.NIGNormalMetamodel(seed=1))
        kl_est = geweke.geweke_kl(bdb, "nig_normal", [['column', 'numerical']], \
            ['column'], [(1,0), (2,0)], 2, 2, 2, 2)
        assert kl_est
        assert len(kl_est) == 3
        assert kl_est[0] == 2
        assert kl_est[1] > 0 # KL should be positive
        assert kl_est[1] < 10
        assert kl_est[2] > 0 # The KL error estimate should be positive too
        assert kl_est[2] < 10

def test_geweke_nig_normal_seriously():
    with bayeslite.bayesdb_open() as bdb:
        import bayeslite.metamodels.nig_normal as normal
        bayeslite.bayesdb_register_metamodel(bdb, normal.NIGNormalMetamodel(seed=1))
        cells = [(i,0) for i in range(4)]
        for chain_ct in (0, 1, 5):
            kl_est = geweke.geweke_kl(bdb, "nig_normal", \
                [['column', 'numerical']], ['column'], cells, \
                200, 200, chain_ct, 3000)
            assert kl_est[0] == 3000
            assert kl_est[1] > 0
            assert kl_est[1] < 0.1
            assert kl_est[2] > 0
            assert kl_est[2] < 0.05
