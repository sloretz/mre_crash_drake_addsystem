#include <drake/systems/framework/leaf_system.h>

#include <pybind11/pybind11.h>

namespace py = pybind11;

using drake::systems::LeafSystem;

class DoNothingSystem : public LeafSystem<double>
{
};

PYBIND11_MODULE(mre, m) {
  m.doc() = "Minimal reproducible example";

  py::module::import("pydrake.systems.framework");

  py::class_<DoNothingSystem, LeafSystem<double>>(m, "DoNothingSystem")
    .def(py::init());
}
