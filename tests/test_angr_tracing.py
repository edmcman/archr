import archr
import os
import unittest

test_location = os.path.dirname(os.path.realpath(__file__))


class TestangrTracing(unittest.TestCase):
    @unittest.skipUnless(archr._angr_available, "angr required")
    def test_angr_tracing(self):
        target = archr.targets.LocalTarget(os.path.join(test_location, '../../binaries/tests/x86_64/true'))
        dsb = archr.analyzers.DataScoutAnalyzer(target)
        apb = archr.analyzers.angrProjectAnalyzer(target, dsb)
        asb = archr.analyzers.angrStateAnalyzer(target, apb)
        qtb = archr.analyzers.QEMUTracerAnalyzer(target)

        trace = qtb.fire()
        p = apb.fire()
        s = asb.fire()

        # Better place to do this?
        import angr

        tech = trace.tracer_technique(mode=angr.exploration_techniques.tracer.TracingMode.Permissive, copy_states=True)
        simgr = p.factory.simulation_manager(s)
        simgr.use_technique(tech)
        simgr.run()

        assert len(simgr.traced) == 1


if __name__ == '__main__':
    unittest.main()
