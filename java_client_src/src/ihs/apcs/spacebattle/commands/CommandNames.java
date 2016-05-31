package ihs.apcs.spacebattle.commands;

/**
 * Enum for matching Command Names for Command Queue Short Names.
 * 
 * e.g. env.getShipStatus().getCommandQueue()[0].equals(CommandNames.ThrustCommand.toString())
 * 
 * @author Michael A. Hawker
 * 
 * @since 1.2
 */
public enum CommandNames {
	AllStop {
		public String toString() {
			return "STOP";
		}
	},
	Brake {
		public String toString() {
			return "BRAKE";
		}
	},
	Cloak {
		public String toString() {
			return "CLOAK";
		}
	},
	Collect {
		public String toString() {
			return "COLCT";
		}
	},
	DeployLaserBeacon {
		public String toString() {
			return "DLBN";
		}
	},
	DeploySpaceMine {
		public String toString() {
			return "MINE";
		}
	},
	DestroyAllLaserBeacons {
		public String toString() {
			return "DAYLB";
		}
	},
	Eject {
		public String toString() {
			return "EJECT";
		}
	},
	FireTorpedo {
		public String toString() {
			return "FIRE";
		}
	},
	Idle {
		public String toString() {
			return "IDLE";
		}
	},
	LowerEnergyScoop {
		public String toString() {
			return "SCOOP";
		}
	},
	Radar {
		public String toString() {
			return "RADAR";
		}
	},
	RaiseShields {
		public String toString() {
			return "SHLD";
		}
	},
	Repair {
		public String toString() {
			return "REP";
		}
	},
	Rotate {
		public String toString() {
			return "ROT";
		}
	},
	Scan {
		public String toString() {
			return "DQSCN";
		}
	},
	Steer {
		public String toString() {
			return "STEER";
		}
	},
	Thrust {
		public String toString() {
			return "THRST";
		}
	},
	Warp {
		public String toString() {
			return "WARP";
		}
	}
}