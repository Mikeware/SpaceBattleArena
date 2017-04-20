import { Component, ViewChild, AfterViewInit, ElementRef } from '@angular/core';
import { SocketIOService } from './services/socketioService';
import { RenderService } from "./services/renderService";

@Component({
    selector: 'my-app',
    //styleUrls: ['./app/app.component.css'],
    templateUrl: './app/app.html',
    providers: [SocketIOService, RenderService]
})
export class AppComponent implements AfterViewInit {
    public name = 'Angular';

    @ViewChild('container') container: ElementRef;
    @ViewChild('console') console: ElementRef;

    private loading: boolean = true;

    public constructor(private _socketioService: SocketIOService,
                       private _renderService: RenderService) {
    }

    public ngAfterViewInit(): void {
        this._socketioService.haveData = () => {
            // TODO: Adding loading bool to display message about waiting for connection from client...

            // Only Initialize Render Service Once we Have our Data - TODO: Clean this infrastructure timing/references up.
            this._renderService.init(this.container.nativeElement, this._socketioService);
            this.loading = false;
        };

        // Initialize Connection
        this._socketioService.init(this.console.nativeElement);
    }
}
