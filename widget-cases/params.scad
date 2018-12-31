// Ansible widget cases
//
// Params: sets the we want
// -----------------------------------------------------------------------------

// Overall case
CASE_WIDTH = 90;
CASE_LENGTH = 140;
CASE_HEIGHT = 55;
WALL_THICKNESS = 3;
FLOOR_THICKNESS = WALL_THICKNESS;
SEGMENTS = 60;

// -----------------------------------------------------------------------------

// Front door
FRONT_DOOR_THICKNESS = 3;
FRONT_DOOR_INSET = 1;  // how much gap to give
FRONT_DOOR_OFFSET_Y = 4; // how far in from the edge
FRONT_DOOR_WIDTH = CASE_WIDTH - WALL_THICKNESS - FRONT_DOOR_INSET;
FRONT_DOOR_HEIGHT = CASE_HEIGHT - (WALL_THICKNESS * 2) + (FRONT_DOOR_INSET * 2);

// -----------------------------------------------------------------------------

// Pi shelf
SHELF_THICKNESS = WALL_THICKNESS - 1;
SHELF_Y = 52;
SHELF_LENGTH = 40;
SHELF_HEIGHT = 28;
SHELF_PEG_OFFSET_X = 3.5;
SHELF_PEG_OFFSET_Y = 3.0;
SHELF_PEG_HEIGHT = 4;
SHELF_PEG_RADIUS_BASE = 2.5 / 2;
SHELF_PEG_RADIUS_TOP = 1.75 / 2;

// -----------------------------------------------------------------------------

// Lid
LID_THICKNESS = WALL_THICKNESS;
DOCK_BORDER_HEIGHT = 9;
DOCK_BORDER_THICKNESS = 4;
DOCK_INSET = 2;

// Lid ridge
RIDGE_THICKNESS = WALL_THICKNESS * 2;
RIDGE_PEG_HEIGHT = 4;
RIDGE_PEG_RADIUS_BASE = 2.5 / 2;
RIDGE_PEG_RADIUS_TOP = 1.75 / 2;
RIDGE_PEG_RADIUS_HOLE = 2.3 / 2;
RIDGE_PEG_OFFSET = 5;

// -----------------------------------------------------------------------------

// General mount
MOUNT_HEIGHT = 15;
MOUNT_THICKNESS = 3;
MOUNT_SEGMENTS = 360;
GRIP_HEIGHT = 5;
GRIP_THICKNESS = 7;
LABEL_MOUNT_HEIGHT = 1;
LABEL_MOUNT_FONT_SIZE = 6;
LABEL_MOUNT_FONT = "Avenir Pro:style=Bold";

// Selector dock
SELECTOR_DOCK_Y = CASE_LENGTH * .78;
SELECTOR_DOCK_RADIUS = 18;
SELECTOR_DOCK_BORDER_RADIUS = SELECTOR_DOCK_RADIUS + DOCK_BORDER_THICKNESS;
SELECTOR_HOLE_OFFSET = DOCK_BORDER_THICKNESS;
SELECTOR_HOLE_SIZE = SELECTOR_DOCK_RADIUS - SELECTOR_HOLE_OFFSET;
SELECTOR_LABEL_Y = -SELECTOR_DOCK_RADIUS - 2;

// Selector mount
SELECTOR_MOUNT_COLOR = [0.6, 0.6, 0.8];
SELECTOR_MOUNT_OFFSET = 0.5;
SELECTOR_MOUNT_THICKNESS = WALL_THICKNESS;
SELECTOR_MOUNT_RADIUS = SELECTOR_DOCK_RADIUS - SELECTOR_MOUNT_OFFSET;
SELECTOR_HOLE_RADIUS = SELECTOR_MOUNT_RADIUS - SELECTOR_HOLE_OFFSET;

// Widget dock
WIDGET_DOCK_Y = CASE_LENGTH * .15;
WIDGET_DOCK_SIZE = 32;
WIDGET_BORDER_RADIUS = 2.5;
WIDGET_HOLE_OFFSET = DOCK_BORDER_THICKNESS * 2;
WIDGET_HOLE_SIZE = WIDGET_DOCK_SIZE - WIDGET_HOLE_OFFSET;

// Widget mount
WIDGET_MOUNT_COLOR = [0.8, 0.6, 0.6];
WIDGET_MOUNT_OFFSET = 1;
WIDGET_MOUNT_THICKNESS = WALL_THICKNESS;
WIDGET_MOUNT_SIZE = WIDGET_DOCK_SIZE - WIDGET_MOUNT_OFFSET;
WIDGET_MOUNT_HOLE_SIZE = WIDGET_MOUNT_SIZE - WIDGET_HOLE_OFFSET;

// -----------------------------------------------------------------------------

// Pi
PI_COLOR = [0.3, 0.4, 0.3];
PI_Y = SHELF_Y + 5;
PI_WIDTH = 66.04;
PI_LENGTH = 30.48;
PI_DEPTH = 1.5;
PI_HOLE_RADIUS = 2 / 2;
PI_HOLE_OFFSET_X = 3.5;
PI_HOLE_OFFSET_Y = 3.0;

// Battery pack
BATTERY_COLOR = [0.2, 0.2, 0.2];
BATTERY_WIDTH = 68.58;
BATTERY_LENGTH = 96.52;
BATTERY_DEPTH = 22.86;

BATTERY_DIAMETER = 23;

BATTERY_GUIDE_OFFSET_X = -5.5;
BATTERY_GUIDE_WIDTH = 4;
BATTERY_GUIDE_HEIGHT = 4;
BATTERY_GUIDE_LENGTH = CASE_LENGTH * .65;

// -----------------------------------------------------------------------------

// Magnet selector

MAGNET_BOARD_WIDTH = 23;
MAGNET_BOARD_HEIGHT = 21;

MAGNET_HOLE_OFFSET = 2;
MAGNET_HOLE_WIDTH = MAGNET_BOARD_WIDTH - MAGNET_HOLE_OFFSET;
MAGNET_HOLE_LENGTH = 10.5;

MAGNET_BOARD_INSET = 1;
MAGNET_BOARD_INSET_WIDTH = MAGNET_BOARD_WIDTH + MAGNET_BOARD_INSET;
MAGNET_BOARD_INSET_HEIGHT = MAGNET_BOARD_HEIGHT + MAGNET_BOARD_INSET;
MAGNET_BOARD_INSET_DEPTH = 1;

MAGNET_PEG_HEIGHT = 4;
MAGNET_PEG_RADIUS_BASE = 2.5 / 2;
MAGNET_PEG_RADIUS_TOP = 1.75 / 2;
MAGNET_PEG_OFFSET_X = -0.25;
MAGNET_PEG_OFFSET_Y = 0.7;
MAGNET_PEG_OFFSET_Z = -MAGNET_BOARD_INSET;

MAGNET_PEG_HOLE_RADIUS = 2.5 / 2;
MAGNET_PEG_HOLE_OFFSET_X = 1 + MAGNET_PEG_HOLE_RADIUS;
MAGNET_PEG_HOLE_OFFSET_Y = 1 + MAGNET_PEG_HOLE_RADIUS;

// -----------------------------------------------------------------------------

// Light selector

LIGHT_BOARD_WIDTH = 19;
LIGHT_BOARD_HEIGHT = 16;

LIGHT_HOLE_OFFSET = 2;
LIGHT_HOLE_WIDTH = LIGHT_BOARD_WIDTH - LIGHT_HOLE_OFFSET;
LIGHT_HOLE_LENGTH = 8;

LIGHT_BOARD_INSET = 1;
LIGHT_BOARD_INSET_WIDTH = LIGHT_BOARD_WIDTH + LIGHT_BOARD_INSET;
LIGHT_BOARD_INSET_HEIGHT = LIGHT_BOARD_HEIGHT + LIGHT_BOARD_INSET;
LIGHT_BOARD_INSET_DEPTH = 1;

LIGHT_PEG_HEIGHT = 4;
LIGHT_PEG_RADIUS_BASE = 2.5 / 2;
LIGHT_PEG_RADIUS_TOP = 1.75 / 2;
LIGHT_PEG_OFFSET_X = 1.65;
LIGHT_PEG_OFFSET_Y = 3.65;
LIGHT_PEG_OFFSET_Z = -LIGHT_BOARD_INSET;

LIGHT_PEG_HOLE_RADIUS = 2.3 / 2;
LIGHT_PEG_HOLE_OFFSET_X = 1 + LIGHT_PEG_HOLE_RADIUS;
LIGHT_PEG_HOLE_OFFSET_Y = 1.5 + LIGHT_PEG_HOLE_RADIUS;
