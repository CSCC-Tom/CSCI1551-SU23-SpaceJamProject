from panda3d.core import Loader, PandaNode, NodePath, Vec3, LColor
from Classes import SpaceJamFunctions
from Classes.GameObjects.GameModel import ModelObject
from Classes.GameObjects.ModelWithCollider import (
    ModelWithSphereCollider,
    ModelWithCapsuleCollider,
)

# Script containing primarily "end leaf" classes for SpaceJam that are not inherited by anything, and are generally small.
# (Large classes belong in their own script files!)


class SpaceJamUniverse(ModelWithSphereCollider):
    """ObjectWithModel representing the Universe (skybox)"""

    def __init__(self, loader: Loader, scene_node: NodePath):
        ModelWithSphereCollider.__init__(
            self, loader, "./Assets/Universe/Universe.obj", scene_node, "Universe", True
        )
        self.modelNode.setScale(90000)


class SpaceJamPlanet(ModelWithSphereCollider):
    """SphereCollidableObject representing a Planet"""

    def __init__(
        self,
        loader: Loader,
        model_path: str,
        parent_node: NodePath,
        node_name: str,
        position: Vec3,
        scale: float,
    ):
        ModelWithSphereCollider.__init__(
            self, loader, model_path, parent_node, node_name
        )

        # Note position of 0 above to make sure the collider matches visual position, and then both are moved by moving the parent modelNode.
        self.modelNode.setPos(position)
        # Note scale of 1 above to make sure the collider matches visual size, and THEN we scale both up together by scaling the parent modelNode.
        self.modelNode.setScale(scale)


class SpaceJamSolarSystem(PandaNode):
    """PandaNode container of all the Planets in the Universe. Currently contains Sun, Mercury, and BBQ"""

    def __init__(self, loader: Loader, parent_node: NodePath):
        super(SpaceJamSolarSystem, self).__init__("Solar System")

        self.sun = SpaceJamPlanet(
            loader,
            "./Assets/Planets/protoPlanet.obj",
            parent_node,
            "Sun",
            (0, 0, 0),
            20,
        )
        self.sun.replaceTextureOnModel(loader, "./Assets/Planets/geomPatterns2.png")

        self.mercury = SpaceJamPlanet(
            loader,
            "./Assets/Planets/protoPlanet.obj",
            parent_node,
            "Mercury",
            (30, 20, 10),
            7,
        )
        self.mercury.replaceTextureOnModel(loader, "./Assets/Planets/geomPatterns2.png")
        self.mercury.modelNode.setColorScale((1.0, 0.75, 0.75, 1.0))

        self.bbq = SpaceJamPlanet(
            loader,
            "./Assets/Planets/protoPlanet.obj",
            parent_node,
            "BBQ",
            (50, 40, 30),
            14,
        )
        self.bbq.replaceTextureOnModel(loader, "./Assets/Planets/bbq.jpeg")


class SpaceJamBase(ModelWithCapsuleCollider):
    """SphereCollidableObject that also manages a swarm of Defenders"""

    def __init__(self, loader: Loader, parent_node: NodePath, pos: Vec3):
        ModelWithCapsuleCollider.__init__(
            self,
            loader,
            "./Assets/Universe/Universe.obj",
            parent_node,
            "SpaceBase",
            (0, 0, 0),
            (0.75, 0, 0),
        )
        self.baseModelB = ModelObject(
            loader, "./Assets/Universe/Universe.obj", self.modelNode, "SpaceBaseB"
        )
        self.baseModelB.modelNode.setPos((0.75, 0, 0))
        self.modelNode.setPos(pos)
        self.modelNode.setScale(1.5)

        self.defenders: list[SpaceJamDefender] = []
        self.spawnDefenders(loader, self.modelNode, 100, 0, (1, 0, 0, 1))
        self.spawnDefenders(loader, self.modelNode, 100, 1, (0, 1, 0, 1))
        # print("Space Jam Base placed at " + str(pos))

    def spawnDefenders(
        self,
        loader: Loader,
        parent_node: NodePath,
        count: int,
        pattern: int,
        color_tint: LColor,
    ):
        """Spawns the defenders around the base by way of the given pattern. pattern 0 is a line, pattern 1 is a line of lines. Spawned defenders are added to the base's list."""
        if pattern == 0:
            def_positions = SpaceJamFunctions.CreateLinePatternPositionsList(
                count, Vec3(0, 0, 0), Vec3(1, 1, -1)
            )
        elif pattern == 1:
            def_positions = SpaceJamFunctions.CreateLineOfLinePatternsPositionsList(
                int(count * 0.5),
                int(count * 0.5),
                Vec3(0, 0, 0),
                Vec3(-1, 0, 1),
                Vec3(1, -1, -1),
            )
        for pos in def_positions:
            # print("Spawned defender in pattern " + str(pattern) + " at pos " + str(pos))
            self.defenders.append(
                SpaceJamDefender(
                    loader,
                    parent_node,
                    pos,
                    color_tint,
                    parent_node.name + "def" + str(len(self.defenders)),
                )
            )


class SpaceJamDefender(ModelWithSphereCollider):
    """Object spawned and managed by a Base that has a model and collider"""

    def __init__(
        self,
        loader: Loader,
        parent_node: NodePath,
        pos: Vec3,
        col_tint: LColor,
        node_name: str,
    ):
        ModelWithSphereCollider.__init__(
            self,
            loader,
            "./Assets/Planets/protoPlanet.obj",
            parent_node,
            node_name + "Model",
        )

        self.modelNode.setScale(0.5)
        self.modelNode.setPos(pos)
        self.modelNode.setColorScale(col_tint)
        # print("Spawned Defender(" + node_name + ")")
