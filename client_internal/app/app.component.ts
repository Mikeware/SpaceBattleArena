import { Component } from '@angular/core';
import { SocketIOService } from './services/socketioService';

@Component({
    selector: 'my-app',
    templateUrl: './app/app.html',
    providers: [SocketIOService]
})
export class AppComponent { 
    public name = 'Angular';

    public constructor(private _socketioService: SocketIOService) {
        this._socketioService.init();
    }
}
