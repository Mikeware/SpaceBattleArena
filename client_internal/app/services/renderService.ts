import * as THREE from "three";
import * as TrackballControls from "three-trackballcontrols";
import * as TWEEN from "tween.js";
import { SocketIOService } from "./socketioService";
import { RectangleOutline } from "../utils/RectangleOutline";
//import Stats = require('stats.js');

export class RenderService {
    //private stats: Stats;
    private scene: THREE.Scene;
    private camera: THREE.PerspectiveCamera;
    private renderer: THREE.WebGLRenderer;
    private controls: TrackballControls;
    private ship: THREE.Mesh;

    private io: SocketIOService;

    public init(container: HTMLElement,
                socketService: SocketIOService) { // TODO: Architect better sharing of the data...
        //this.addStats();

        this.io = socketService;

        const width = window.innerWidth;
        const height = window.innerHeight;

        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(45, width/height);
        this.camera.position.set(this.io.request.WORLDWIDTH / 2, this.io.request.WORLDHEIGHT / 2, 900); // TODO: Set Z based on aspect/viewport and worldsize

        this.renderer = new THREE.WebGLRenderer({antialias: true});
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.setSize(width, height);
        this.renderer.setClearColor(0x000000);

        container.appendChild(this.renderer.domElement);
        //this.controls = new TrackballControls(this.camera, container);

        // Ship
        const textureLoader = new THREE.TextureLoader();
        textureLoader.load('assets/Ships/ship0.png', t => { // TODO: Manage loading of multiple textures better... :( (or at least object data/position update dependency from environment)
            t.wrapS = t.wrapT = THREE.RepeatWrapping;
            t.repeat.set(1 / 7, 1 / 2); // TODO: This doesn't work.

            let size = this.io.environment.SHIPDATA.HITRADIUS; // TODO: Find actual property needed for size?
            let geometry = new THREE.CubeGeometry(size, size, 0.1);
            let material = new THREE.MeshLambertMaterial({map: t});
            this.ship = new THREE.Mesh(geometry, material);

            this.scene.add(this.ship);

            // Add Outline of world boundaries for now
            let rect = new RectangleOutline(this.io.request.WORLDWIDTH, this.io.request.WORLDHEIGHT)
            rect.translateZ(1);
            this.scene.add(rect);

            // Lights
            const ambientLight = new THREE.AmbientLight(0xcccccc);
            this.scene.add(ambientLight);

            const pointLight = new THREE.PointLight(0xffffff);
            pointLight.position.set(300, 0, 300);
            this.scene.add(pointLight);

            // start animation
            this.animate();

            // bind to window resizes
            window.addEventListener('resize', _ => this.onResize());
        });        
    }

    public addStats() {
        //this.stats = new Stats();
        //document.body.appendChild(this.stats.dom);
    }

    public addStars(starsCount: number) {
        const stars = new THREE.Geometry();
        const starMaterial = new THREE.PointCloudMaterial({color: 0xffffff});

        for (let i = 0; i < starsCount; i++) {
            let x = Math.random() * 2000 - 1000;
            let y = Math.random() * 2000 - 1000;
            let z = Math.random() * 2000 - 1000;

            let star = new THREE.Vector3(x, y, z);

            stars.vertices.push(star);
        }

        let pointCloud = new THREE.PointCloud(stars, starMaterial);
        this.scene.add(pointCloud);
    }

    public updateScale(newScale: number) {
        const that = this;
        new TWEEN.Tween({scale: this.ship.scale.x})
            .to({scale: newScale}, 1000)
            .easing(TWEEN.Easing.Elastic.InOut)
            .onUpdate(function () {
                that.ship.scale.set(this.scale, this.scale, this.scale);
            })
            .start();
    }

    public animate() {
        window.requestAnimationFrame(() => { 
            this.animate(); 
        });

        this.ship.position.x = this.io.environment.SHIPDATA.POSITION[0];
        this.ship.position.y = this.io.request.WORLDHEIGHT - this.io.environment.SHIPDATA.POSITION[1];
        this.ship.rotation.z = Math.radians(this.io.environment.SHIPDATA.ROTATION - 90);

        //this.stats.update();
        //this.controls.update();
        TWEEN.update();

        this.renderer.render(this.scene, this.camera);
    }

    public onResize() {
        const width = window.innerWidth;
        const height = window.innerHeight - 90;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();

        this.renderer.setSize(width, height);

        // TODO: Adjust camera position?
    }
}
