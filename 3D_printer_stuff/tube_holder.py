import cadquery as cq


class FilamentGuide:

    def __init__(self, outer_diameter: float = 4, inner_diameter: float = 2.5 + .4,
                 height: float = 18, segment_width: float = 13, padding: float = 4, padding_x: float = None,
                 tip_length: float = 10, tip_height: float = 5, screw_inner_diameter=3.8, screw_outer_diameter=8,
                 screw_head=3.3):
        self.screw_head = screw_head
        self.screw_outer_radius = screw_outer_diameter / 2
        self.screw_inner_radius = screw_inner_diameter / 2
        self.tip_height = tip_height
        self.tip_length = tip_length
        self.depth = height / 2 - 3
        self.segment_width: float = segment_width
        self.padding: float = padding
        self.padding_x: float = padding_x
        self.inner_radius: float = inner_diameter / 2
        self.height: float = height
        self.outer_radius: float = outer_diameter / 2
        self.segments: list[str] = []
        self.main: cq.Workplane = cq.Workplane("XY")
        self.body: cq.Workplane = self.main.workplane()
        self.texts: list[cq.Shape] = []

    def add_segment(self, segment):
        self.segments.append(segment)
        return self

    def render(self):
        self.body = self.body.box(self._calculate_length(), self._calculate_width(), self.height)

        for i in range(self.segments.__len__()):
            self._add_segment(i)

        text = cq.Compound.makeCompound(self.texts).rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90).translate(
            cq.Vector(0, -self._calculate_width() / 2, 0))
        text.label = "text"

        self.body = self.body.cut(text)

        self._add_tip()
        self._add_tip(-1)

        body = cq.Compound.makeCompound(self.body.val())
        body.label = "body"

        show_object(body)
        show_object(text)

        assembly = cq.Assembly()
        assembly.add(body, name="body", color=cq.Color("black"))
        assembly.add(text, name="text", color=cq.Color("white"))

        assembly.constrain("body", cq.Vertex.makeVertex(100, 100, -100), "text",
                           cq.Vertex.makeVertex(100, 100, -100), "Point")
        assembly.constrain("body", cq.Vertex.makeVertex(100, -100, 100), "text",
                           cq.Vertex.makeVertex(100, -100, 100), "Point")
        assembly.constrain("body", cq.Vertex.makeVertex(-100, 100, 100), "text",
                           cq.Vertex.makeVertex(-100, 100, 100), "Point")
        assembly.solve()
        assembly.save("tube_holder.step")

        cq.exporters.export(cq.Compound.makeCompound([body, text]).rotate([0, 0, 0], [1, 0, 0], -90), "tube_holder.3mf",
                            tolerance=0.01, angularTolerance=0.1)

    def _add_tip(self, direction=1):
        offset = direction * (self._calculate_length() / 2 + self.tip_length / 2)
        self.body = self.body.faces(">Y").workplane(offset=-self._calculate_width() / 2).move(-offset, self.height / 2).box(self.tip_length, self.height, self._calculate_width())
        self.body = self.body.faces(">Y")
        self.body = self.body.workplane().move(-offset, self.height / 2).circle(self.screw_inner_radius).cutThruAll()
        self.body = self.body.faces("<Y").workplane().move(offset, self.height / 2).circle(4).cutBlind(-(self._calculate_width()-(self.tip_height+self.screw_head/2-.1)))
        self.body = self.body.workplane().cut(
            cq.Solid.makeCone(self.screw_inner_radius, self.screw_outer_radius, self.screw_head).translate(
                [offset, 0, -self._calculate_width() + self.tip_height + self.screw_head]).rotate([0, 0, 0], [1, 0, 0],
                                                                                                  90))

    def _is_gui(self):
        return hasattr(self.__class__, "show_object") and callable(getattr(self.__class__, "show_object"))

    def _calculate_width(self):
        return self.outer_radius + 2 * self.padding

    def _calculate_length(self):
        return self.segments.__len__() * self.segment_width

    def _add_segment(self, i):
        placement = self.segment_width / 2 + i * self.segment_width
        offset = (self.segments.__len__() * self.segment_width) / 2
        self.body = self.body.faces("<Z").workplane(centerOption="CenterOfBoundBox").moveTo(placement - offset).circle(
            self.outer_radius).cutBlind(-self.depth).faces(">Z").workplane(centerOption="CenterOfBoundBox").moveTo(
            placement - offset).circle(
            self.outer_radius).cutBlind(-self.depth).faces("<Z").workplane(centerOption="CenterOfBoundBox").moveTo(
            placement - offset).circle(
            self.inner_radius).cutThruAll().last()

        self.texts.append(self.main.workplane(
            origin=cq.Vector(placement - offset, 0, 0)).text(self.segments[i], self.height * .5, -.2,
                                                             combine=False).val())


if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass

FilamentGuide().add_segment("1").add_segment("2").add_segment("3").add_segment("4").add_segment("5").render()
