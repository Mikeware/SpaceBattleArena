import * as THREE from "three";

export class RectangleOutline extends THREE.Line {
    constructor(width: number, height: number, parameters?: THREE.LineBasicMaterialParameters) {
        if (!parameters)
        {
            parameters = { color: 0xffffff, linewidth: 1 };
        }

        // geometry
        var geometry = new THREE.Geometry();
        geometry.vertices.push( new THREE.Vector3( 0, 0, 0 ) );
        geometry.vertices.push( new THREE.Vector3( width, 0, 0 ) );
        geometry.vertices.push( new THREE.Vector3( width, height, 0 ) );
        geometry.vertices.push( new THREE.Vector3( 0, height, 0 ) );
        geometry.vertices.push( new THREE.Vector3( 0, 0, 0 ) ); // close the loop

        // material
        var material = new THREE.LineBasicMaterial( parameters );

        // line
        super( geometry, material );
    }
}