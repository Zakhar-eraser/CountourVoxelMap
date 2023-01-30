import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
from structures.route import route_idx2pos
from visualizer.common.visualizer_geometry import make_route_lines
from structures.destination_list import get_marks

class OutputWindow:

    def __init__(self, voxel_grid, occupancy_grid, route_idx, targets):
        vx = voxel_grid
        self._vs = vx.voxel_size
        self._grid = occupancy_grid
        self.route = route_idx2pos(route_idx)
        self.route_idx = route_idx

        app = gui.Application.instance
        self._window = app.create_window("Calculated route", 1024, 640)
        self._widget3d = gui.SceneWidget()
        self._window.add_child(self._widget3d)

        # Setting gui`s panel
        em = self._window.theme.font_size
        separation_height = int(round(0.5 * em))
        self._settings_panel = gui.Vert(
            0, gui.Margins(0.25 * em, 0.25 * em, 0.25 * em, 0.25 * em))

        # adding 'optimize' button on gui`s panel
        self._opt_button = gui.Button("Optimize")
        self._opt_button.set_on_clicked(self._on_opt_clicked)
        self._settings_panel.add_fixed(separation_height)
        self._settings_panel.add_child(self._opt_button)

        # adding 'done' button on gui`s panel
        self._done_button = gui.Button("Done")
        self._done_button.set_on_clicked(self._on_done_clicked)
        self._settings_panel.add_fixed(separation_height)
        self._settings_panel.add_child(self._done_button)

        self._window.add_child(self._settings_panel)

        self._window.set_on_layout(self._on_layout)

        self._widget3d.scene = rendering.Open3DScene(self._window.renderer)
        self._widget3d.scene.set_background((0.8, 0.6, 0.6, 1))

        pc_mat = rendering.MaterialRecord()
        pc_mat.shader = "defaultUnlit"
        pc_mat.point_size = 6 * self._window.scaling
        self._widget3d.scene.add_geometry("Point Cloud", vx, pc_mat)

        bounds = self._widget3d.scene.bounding_box
        center = bounds.get_center()
        self._widget3d.setup_camera(60, bounds, center)

        pc_mat.shader = "defaultLit"
        self._markers_count = self._spawn_geometry([get_marks(targets), pc_mat], "mark_")
        self._lines_count = self._spawn_geometry(make_route_lines(self.route, 5, self._vs / 2 + 0.1), "line_")
    
    def _spawn_geometry(self, glist, prefix):
        geom_count = 0
        for geom in glist[0]:
            geom_count += 1
            self._widget3d.scene.add_geometry(prefix + str(geom_count), geom, glist[1])
        return geom_count

    def _on_layout(self, layout_context):
        r = self._window.content_rect
        self._widget3d.frame = r
        width = 17 * layout_context.theme.font_size
        height = min(
            r.height,
            self._settings_panel.calc_preferred_size(
                layout_context, gui.Widget.Constraints()).height)
        self._settings_panel.frame = gui.Rect(r.get_right() - width, r.y, width,
                                              height)
    
    def _on_opt_clicked(self):
        pass

    def _on_done_clicked(self):
        gui.Application.instance.quit()