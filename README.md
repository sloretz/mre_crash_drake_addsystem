# Minimal Reproducable Example of crash in DiagramBuilder.AddSystem with custom Python bindings

* Ubuntu Focal (20.04)
* Drake from source bf2d26e6e5a84c8481c6e6e2cf23edfeba215611
* ROS Rolling Ridley

# Configuring

Either uncomment the two `find_package()` calls for `pybind11` and comment the hack to import Drake's pybind11 version, or do the reverse.
The hack has hardcoded absolute paths that will need to be edited on your machine to match the location of the Drake installation path.

Using the ROS version will require a [ROS Rolling install](https://index.ros.org/doc/ros2/Installation/Rolling/Linux-Install-Debians/).

```
sudo apt install ros-rolling-pybind11-vendor
```

## Building

Build Drake with debug symbols, and install to a binary install folder

```
bazel  run --compilation_mode=dbg -c dbg //:install -- --no_strip /home/sloretz/bigssd/dbg-drake/
```

Create a virtual environment in the Drake install folder and activated

```
python3 -m venv --system-site-packages dbg-drake
```

Create a colcon workspace, and clone this CMake project into it.

```
mkdir ws
mkdir ws/src
cd ws/src
git clone https://github.com/sloretz/mre_crash_drake_addsystem.git
cd ../
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Debug --packages-select mre
```

## Running

Activate the drake workspace; source the built workspace; Run the `run_mre.py` script using gdb

```console
$ . /dbg-drake/bin/activate
(dbg-drake) $ . ws/install/setup.bash
(dbg-drake) $ gdb --ex=r --args python3 ./bigssd/drake_ros_demos/use_drake/mre/run_mre.py
```

## Results

Everything is happy if the version of pybind11 shipped with Drake is used.
If the version of Pybind11 shipped with ROS is used, then everything crashes :(

```
GNU gdb (Ubuntu 9.2-0ubuntu1~20.04) 9.2
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from python3...
Reading symbols from /usr/lib/debug/.build-id/02/526282ea6c4d6eec743ad74a1eeefd035346a3.debug...
Starting program: /home/sloretz/bigssd/dbg-drake/bin/python3 ./bigssd/drake_ros_demos/use_drake/mre/run_mre.py
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
 --- modulename: run_mre, funcname: main
run_mre.py(30):     builder = DiagramBuilder()
run_mre.py(32):     builder.AddSystem(mre.DoNothingSystem())

Program received signal SIGSEGV, Segmentation fault.
0x0000000000000031 in ?? ()
(gdb) bt
#0  0x0000000000000031 in ?? ()
#1  0x00007fffe58d736b in pybind11::detail::move_only_holder_caster<drake::systems::System<double>, std::unique_ptr<drake::systems::System<double>, std::default_delete<drake::systems::System<double> > > >::load_value (this=0x7fffffffc740, v_h=..., load_type=pybind11::detail::LoadType::DerivedCppSinglePySingle) at external/pybind11/include/pybind11/cast.h:1856
#2  0x00007fffe58bf3ab in pybind11::detail::type_caster_generic::load_impl<pybind11::detail::move_only_holder_caster<drake::systems::System<double>, std::unique_ptr<drake::systems::System<double>, std::default_delete<drake::systems::System<double> > > > > (this=0x7fffffffc740, src=..., convert=true) at external/pybind11/include/pybind11/cast.h:810
#3  0x00007fffe58a273c in pybind11::detail::move_only_holder_caster<drake::systems::System<double>, std::unique_ptr<drake::systems::System<double>, std::default_delete<drake::systems::System<double> > > >::load (this=0x7fffffffc740, src=..., convert=true) at external/pybind11/include/pybind11/cast.h:1794
#4  0x00007fffe586952a in pybind11::detail::argument_loader<drake::systems::DiagramBuilder<double>*, std::unique_ptr<drake::systems::System<double>, std::default_delete<drake::systems::System<double> > > >::load_impl_sequence<0ul, 1ul> (this=0x7fffffffc740, call=...) at external/pybind11/include/pybind11/cast.h:2290
#5  0x00007fffe58307c7 in pybind11::detail::argument_loader<drake::systems::DiagramBuilder<double>*, std::unique_ptr<drake::systems::System<double>, std::default_delete<drake::systems::System<double> > > >::load_args (this=0x7fffffffc740, call=...) at external/pybind11/include/pybind11/cast.h:2269
#6  0x00007fffe56ddb12 in pybind11::cpp_function::<lambda(pybind11::detail::function_call&)>::operator()(pybind11::detail::function_call &) const (this=0x0, call=...)
    at external/pybind11/include/pybind11/pybind11.h:162
#7  0x00007fffe56ddc14 in pybind11::cpp_function::<lambda(pybind11::detail::function_call&)>::_FUN(pybind11::detail::function_call &) () at external/pybind11/include/pybind11/pybind11.h:158
#8  0x00007fffe56a9173 in pybind11::cpp_function::dispatcher (self=<PyCapsule at remote 0x7fffe480a1b0>, args_in=
    (<DiagramBuilder_[float] at remote 0x7fffe695cd70>, <mre.DoNothingSystem at remote 0x7fffe4806b70>), kwargs_in=0x0) at external/pybind11/include/pybind11/pybind11.h:654
#9  0x00000000005f4249 in cfunction_call_varargs (kwargs=<optimized out>, args=<optimized out>, func=<built-in method AddSystem of PyCapsule object at remote 0x7fffe480a1b0>) at ../Objects/call.c:772
#10 PyCFunction_Call (func=<built-in method AddSystem of PyCapsule object at remote 0x7fffe480a1b0>, args=<optimized out>, kwargs=<optimized out>) at ../Objects/call.c:772
#11 0x00000000005f46d6 in _PyObject_MakeTpCall (callable=<built-in method AddSystem of PyCapsule object at remote 0x7fffe480a1b0>, args=<optimized out>, nargs=<optimized out>, keywords=<optimized out>)
    at ../Include/internal/pycore_pyerrors.h:13
#12 0x000000000050a9a3 in _PyObject_Vectorcall (kwnames=0x0, nargsf=<optimized out>, args=0x7fffe69d66c8, callable=<built-in method AddSystem of PyCapsule object at remote 0x7fffe480a1b0>)
    at ../Include/cpython/abstract.h:125
#13 _PyObject_Vectorcall (kwnames=0x0, nargsf=<optimized out>, args=0x7fffe69d66c8, callable=<built-in method AddSystem of PyCapsule object at remote 0x7fffe480a1b0>) at ../Include/cpython/abstract.h:115
#14 method_vectorcall (method=<optimized out>, args=0x7fffe69d66d0, nargsf=<optimized out>, kwnames=0x0) at ../Objects/classobject.c:60
#15 0x00000000005749f8 in _PyObject_Vectorcall (callable=<method at remote 0x7ffff7856b40>, args=<optimized out>, nargsf=<optimized out>, kwnames=<optimized out>) at ../Include/cpython/abstract.h:127
#16 0x00000000005724a4 in call_function (kwnames=0x0, oparg=<optimized out>, pp_stack=<synthetic pointer>, tstate=0x9633a0) at ../Python/ceval.c:4960
--Type <RET> for more, q to quit, c to continue without paging--c
#17 _PyEval_EvalFrameDefault (f=<optimized out>, throwflag=<optimized out>) at ../Python/ceval.c:3469
#18 0x00000000005f7146 in PyEval_EvalFrameEx (throwflag=0, f=Frame 0x7fffe69d6550, for file ./bigssd/drake_ros_demos/use_drake/mre/run_mre.py, line 32, in main (builder=<DiagramBuilder_[float] at remote 0x7fffe695cd70>)) at ../Python/ceval.c:741
#19 function_code_fastcall (globals=<optimized out>, nargs=<optimized out>, args=<optimized out>, co=<optimized out>) at ../Objects/call.c:283
#20 _PyFunction_Vectorcall (func=<optimized out>, stack=<optimized out>, nargsf=<optimized out>, kwnames=<optimized out>) at ../Objects/call.c:410
#21 0x00000000005f3d42 in PyVectorcall_Call (kwargs=<optimized out>, tuple=<optimized out>, callable=<function at remote 0x7ffff76c3dc0>) at ../Objects/call.c:1296
#22 PyObject_Call (callable=<function at remote 0x7ffff76c3dc0>, args=<optimized out>, kwargs=<optimized out>) at ../Objects/call.c:227
#23 0x000000000056ca92 in do_call_core (kwdict={}, callargs=(), func=<function at remote 0x7ffff76c3dc0>, tstate=<optimized out>) at ../Python/ceval.c:5010
#24 _PyEval_EvalFrameDefault (f=<optimized out>, throwflag=<optimized out>) at ../Python/ceval.c:3559
#25 0x000000000056955a in PyEval_EvalFrameEx (throwflag=0, f=Frame 0x7ffff779c840, for file /usr/lib/python3.8/trace.py, line 988, in runfunc (args=[], kw={}, self=<Trace(infile=None, outfile=None, ignore=<_Ignore(_mods=set(), _dirs=['/usr', '/home/sloretz/bigssd/dbg-drake'], _ignore={'<string>': 1, 'run_mre': 0}) at remote 0x7ffff76e7c10>, counts={}, pathtobasename={}, donothing=0, trace=1, _calledfuncs={}, _callers={}, _caller_cache={}, start_time=None, globaltrace=<method at remote 0x7ffff78529c0>, localtrace=<method at remote 0x7ffff7856b80>) at remote 0x7ffff76e7c70>, func=<function at remote 0x7ffff76c3dc0>, result=None)) at ../Python/ceval.c:741
#26 _PyEval_EvalCodeWithName (_co=<optimized out>, globals=<optimized out>, locals=<optimized out>, args=<optimized out>, argcount=<optimized out>, kwnames=<optimized out>, kwargs=0x7fffffffd110, kwcount=<optimized out>, kwstep=1, defs=0x0, defcount=0, kwdefs=0x0, closure=0x0, name='runfunc', qualname='Trace.runfunc') at ../Python/ceval.c:4298
#27 0x00000000005f7323 in _PyFunction_Vectorcall (func=<optimized out>, stack=0x7fffffffd100, nargsf=<optimized out>, kwnames=<optimized out>) at ../Objects/call.c:435
#28 0x000000000050a24c in _PyObject_Vectorcall (kwnames=<optimized out>, nargsf=<optimized out>, args=<optimized out>, callable=<optimized out>) at ../Include/cpython/abstract.h:127
#29 method_vectorcall (method=<optimized out>, args=0x7ffff776eaa8, nargsf=<optimized out>, kwnames=<optimized out>) at ../Objects/classobject.c:89
#30 0x00000000005f3d42 in PyVectorcall_Call (kwargs=<optimized out>, tuple=<optimized out>, callable=<method at remote 0x7fffe7060e00>) at ../Objects/call.c:1296
#31 PyObject_Call (callable=<method at remote 0x7fffe7060e00>, args=<optimized out>, kwargs=<optimized out>) at ../Objects/call.c:227
#32 0x000000000056ca92 in do_call_core (kwdict={}, callargs=(<function at remote 0x7ffff76c3dc0>,), func=<method at remote 0x7fffe7060e00>, tstate=<optimized out>) at ../Python/ceval.c:5010
#33 _PyEval_EvalFrameDefault (f=<optimized out>, throwflag=<optimized out>) at ../Python/ceval.c:3559
#34 0x000000000056955a in PyEval_EvalFrameEx (throwflag=0, f=Frame 0x7fffe698bc40, for file ./bigssd/drake_ros_demos/use_drake/mre/run_mre.py, line 23, in wrapped (args=(), kwargs={})) at ../Python/ceval.c:741
#35 _PyEval_EvalCodeWithName (_co=<optimized out>, globals=<optimized out>, locals=<optimized out>, args=<optimized out>, argcount=<optimized out>, kwnames=<optimized out>, kwargs=0x7ffff77ae7b0, kwcount=<optimized out>, kwstep=1, defs=0x0, defcount=0, kwdefs=0x0, closure=(<cell at remote 0x7ffff77d2160>, <cell at remote 0x7ffff76e7d60>), name='main', qualname='main') at ../Python/ceval.c:4298
#36 0x00000000005f7323 in _PyFunction_Vectorcall (func=<optimized out>, stack=0x7ffff77ae7b0, nargsf=<optimized out>, kwnames=<optimized out>) at ../Objects/call.c:435
#37 0x000000000056b26e in _PyObject_Vectorcall (kwnames=0x0, nargsf=<optimized out>, args=0x7ffff77ae7b0, callable=<function at remote 0x7fffe65e8dc0>) at ../Include/cpython/abstract.h:127
#38 call_function (kwnames=0x0, oparg=<optimized out>, pp_stack=<synthetic pointer>, tstate=0x9633a0) at ../Python/ceval.c:4963
#39 _PyEval_EvalFrameDefault (f=<optimized out>, throwflag=<optimized out>) at ../Python/ceval.c:3500
#40 0x000000000056955a in PyEval_EvalFrameEx (throwflag=0, f=Frame 0x7ffff77ae640, for file ./bigssd/drake_ros_demos/use_drake/mre/run_mre.py, line 36, in <module> ()) at ../Python/ceval.c:741
#41 _PyEval_EvalCodeWithName (_co=<optimized out>, globals=<optimized out>, locals=<optimized out>, args=<optimized out>, argcount=<optimized out>, kwnames=<optimized out>, kwargs=0x0, kwcount=<optimized out>, kwstep=2, defs=0x0, defcount=0, kwdefs=0x0, closure=0x0, name=0x0, qualname=0x0) at ../Python/ceval.c:4298
#42 0x000000000068c4a7 in PyEval_EvalCodeEx (closure=0x0, kwdefs=0x0, defcount=0, defs=0x0, kwcount=0, kws=0x0, argcount=0, args=0x0, locals=<optimized out>, globals=<optimized out>, _co=<optimized out>) at ../Python/ceval.c:4327
#43 PyEval_EvalCode (co=<optimized out>, globals=<optimized out>, locals=<optimized out>) at ../Python/ceval.c:718
#44 0x000000000067bc91 in run_eval_code_obj (co=0x7ffff76e6710, globals={'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <SourceFileLoader(name='__main__', path='./bigssd/drake_ros_demos/use_drake/mre/run_mre.py') at remote 0x7ffff780a940>, '__spec__': None, '__annotations__': {}, '__builtins__': <module at remote 0x7ffff78340e0>, '__file__': './bigssd/drake_ros_demos/use_drake/mre/run_mre.py', '__cached__': None, 'mre': <module at remote 0x7ffff76ca4a0>, 'DiagramBuilder': <pybind11_type(__init__=<instancemethod at remote 0x7fffe480a0d0>, __doc__='DiagramBuilder is a factory class for Diagram. It is single use: after\ncalling Build or BuildInto, DiagramBuilder gives up ownership of the\nconstituent systems, and should therefore be discarded.\n\nA system must be added to the DiagramBuilder with AddSystem before it\ncan be wired up in any way. Every system must have a unique, non-empty\nname.', __module__='pydrake.systems.framework', _original_name='_TemporaryName_N5drake7systems14DiagramBuilderIdEE', _original_qualname='_TemporaryName_N5drake7systems14D...(truncated), locals={'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <SourceFileLoader(name='__main__', path='./bigssd/drake_ros_demos/use_drake/mre/run_mre.py') at remote 0x7ffff780a940>, '__spec__': None, '__annotations__': {}, '__builtins__': <module at remote 0x7ffff78340e0>, '__file__': './bigssd/drake_ros_demos/use_drake/mre/run_mre.py', '__cached__': None, 'mre': <module at remote 0x7ffff76ca4a0>, 'DiagramBuilder': <pybind11_type(__init__=<instancemethod at remote 0x7fffe480a0d0>, __doc__='DiagramBuilder is a factory class for Diagram. It is single use: after\ncalling Build or BuildInto, DiagramBuilder gives up ownership of the\nconstituent systems, and should therefore be discarded.\n\nA system must be added to the DiagramBuilder with AddSystem before it\ncan be wired up in any way. Every system must have a unique, non-empty\nname.', __module__='pydrake.systems.framework', _original_name='_TemporaryName_N5drake7systems14DiagramBuilderIdEE', _original_qualname='_TemporaryName_N5drake7systems14D...(truncated)) at ../Python/pythonrun.c:1125
#45 0x000000000067bd0f in run_mod (mod=<optimized out>, filename=<optimized out>, globals={'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <SourceFileLoader(name='__main__', path='./bigssd/drake_ros_demos/use_drake/mre/run_mre.py') at remote 0x7ffff780a940>, '__spec__': None, '__annotations__': {}, '__builtins__': <module at remote 0x7ffff78340e0>, '__file__': './bigssd/drake_ros_demos/use_drake/mre/run_mre.py', '__cached__': None, 'mre': <module at remote 0x7ffff76ca4a0>, 'DiagramBuilder': <pybind11_type(__init__=<instancemethod at remote 0x7fffe480a0d0>, __doc__='DiagramBuilder is a factory class for Diagram. It is single use: after\ncalling Build or BuildInto, DiagramBuilder gives up ownership of the\nconstituent systems, and should therefore be discarded.\n\nA system must be added to the DiagramBuilder with AddSystem before it\ncan be wired up in any way. Every system must have a unique, non-empty\nname.', __module__='pydrake.systems.framework', _original_name='_TemporaryName_N5drake7systems14DiagramBuilderIdEE', _original_qualname='_TemporaryName_N5drake7systems14D...(truncated), locals={'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <SourceFileLoader(name='__main__', path='./bigssd/drake_ros_demos/use_drake/mre/run_mre.py') at remote 0x7ffff780a940>, '__spec__': None, '__annotations__': {}, '__builtins__': <module at remote 0x7ffff78340e0>, '__file__': './bigssd/drake_ros_demos/use_drake/mre/run_mre.py', '__cached__': None, 'mre': <module at remote 0x7ffff76ca4a0>, 'DiagramBuilder': <pybind11_type(__init__=<instancemethod at remote 0x7fffe480a0d0>, __doc__='DiagramBuilder is a factory class for Diagram. It is single use: after\ncalling Build or BuildInto, DiagramBuilder gives up ownership of the\nconstituent systems, and should therefore be discarded.\n\nA system must be added to the DiagramBuilder with AddSystem before it\ncan be wired up in any way. Every system must have a unique, non-empty\nname.', __module__='pydrake.systems.framework', _original_name='_TemporaryName_N5drake7systems14DiagramBuilderIdEE', _original_qualname='_TemporaryName_N5drake7systems14D...(truncated), flags=<optimized out>, arena=<optimized out>) at ../Python/pythonrun.c:1147
#46 0x000000000067bdcb in PyRun_FileExFlags (fp=0x961240, filename_str=<optimized out>, start=<optimized out>, globals={'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <SourceFileLoader(name='__main__', path='./bigssd/drake_ros_demos/use_drake/mre/run_mre.py') at remote 0x7ffff780a940>, '__spec__': None, '__annotations__': {}, '__builtins__': <module at remote 0x7ffff78340e0>, '__file__': './bigssd/drake_ros_demos/use_drake/mre/run_mre.py', '__cached__': None, 'mre': <module at remote 0x7ffff76ca4a0>, 'DiagramBuilder': <pybind11_type(__init__=<instancemethod at remote 0x7fffe480a0d0>, __doc__='DiagramBuilder is a factory class for Diagram. It is single use: after\ncalling Build or BuildInto, DiagramBuilder gives up ownership of the\nconstituent systems, and should therefore be discarded.\n\nA system must be added to the DiagramBuilder with AddSystem before it\ncan be wired up in any way. Every system must have a unique, non-empty\nname.', __module__='pydrake.systems.framework', _original_name='_TemporaryName_N5drake7systems14DiagramBuilderIdEE', _original_qualname='_TemporaryName_N5drake7systems14D...(truncated), locals={'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <SourceFileLoader(name='__main__', path='./bigssd/drake_ros_demos/use_drake/mre/run_mre.py') at remote 0x7ffff780a940>, '__spec__': None, '__annotations__': {}, '__builtins__': <module at remote 0x7ffff78340e0>, '__file__': './bigssd/drake_ros_demos/use_drake/mre/run_mre.py', '__cached__': None, 'mre': <module at remote 0x7ffff76ca4a0>, 'DiagramBuilder': <pybind11_type(__init__=<instancemethod at remote 0x7fffe480a0d0>, __doc__='DiagramBuilder is a factory class for Diagram. It is single use: after\ncalling Build or BuildInto, DiagramBuilder gives up ownership of the\nconstituent systems, and should therefore be discarded.\n\nA system must be added to the DiagramBuilder with AddSystem before it\ncan be wired up in any way. Every system must have a unique, non-empty\nname.', __module__='pydrake.systems.framework', _original_name='_TemporaryName_N5drake7systems14DiagramBuilderIdEE', _original_qualname='_TemporaryName_N5drake7systems14D...(truncated), closeit=1, flags=0x7fffffffd7b8) at ../Python/pythonrun.c:1063
#47 0x000000000067de4e in PyRun_SimpleFileExFlags (fp=0x961240, filename=<optimized out>, closeit=1, flags=0x7fffffffd7b8) at ../Python/pythonrun.c:428
#48 0x00000000006b6032 in pymain_run_file (cf=0x7fffffffd7b8, config=0x962760) at ../Modules/main.c:381
#49 pymain_run_python (exitcode=0x7fffffffd7b0) at ../Modules/main.c:606
#50 Py_RunMain () at ../Modules/main.c:685
#51 0x00000000006b63bd in Py_BytesMain (argc=<optimized out>, argv=<optimized out>) at ../Modules/main.c:739
#52 0x00007ffff7dcb0b3 in __libc_start_main (main=0x4eea30 <main>, argc=2, argv=0x7fffffffd998, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7fffffffd988) at ../csu/libc-start.c:308
#53 0x00000000005fa4de in _start () at ../Objects/bytesobject.c:2560
```
