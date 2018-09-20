/*
 *  Copyright (C) 1997-2016 JDE Developers Team
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see http://www.gnu.org/licenses/.
 *
 *  Authors : Francisco Miguel Rivas Montero <franciscomiguel.rivas@urjc.es>
 */

#ifndef VISUALIZATION_ICE
#define VISUALIZATION_ICE

#include <jderobot/common.ice>
#include <jderobot/primitives.ice>
#include <jderobot/pose3d.ice>

module jderobot{

	struct Color{
	    float r;
	    float g;
	    float b;
	};

	struct RGBSegment{
	    Segment seg;
	    Color c;
	};

	sequence<RGBSegment> Segments;
	sequence<RGBPoint> Points;
  sequence<byte> File;

	struct bufferSegments{
		Segments buffer;
		bool refresh;
	};

	struct bufferPoints{
		Points buffer;
		bool refresh;
	};

  struct object3d {
    string obj;
    string id;
    string format;
  };

  struct PoseObj3D{
    string id;
    Pose3DData pos;
  };

  sequence<PoseObj3D> bufferPoseObj3D;

  /**
   * Interface to the Visualization interaction.
   */
	interface Visualization
	{
        void drawSegment(bufferSegments bseg);
	      bufferSegments getSegment ();
        void drawPoint(bufferPoints bpnts);
	      bufferPoints getPoints();
        object3d getObj3D(string id);
        bufferPoseObj3D getPoseObj3DData();
        void clearAll();
	};
};
#endif
