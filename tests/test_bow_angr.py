import archr
import os

def setup_module():
    os.system("cd %s/dockers; ./build_all.sh" % os.path.dirname(__file__))

def test_env_angr():
    t = archr.targets.DockerImageTarget('archr-test:entrypoint-env').build().start()
    mb = archr.bows.MemoryMapBow(t)
    apb = archr.bows.angrProjectBow(t, mb)
    asb = archr.bows.angrStateBow(t, apb)
    project = apb.fire()
    assert all(obj.binary.startswith(t.local_path) for obj in project.loader.all_elf_objects[1:])
    state = asb.fire()
    initial_stack = state.solver.eval(state.memory.load(state.regs.rsp, 200), cast_to=bytes)
    assert b"ARCHR=YES" in initial_stack

if __name__ == '__main__':
    test_env_angr()