import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent }  from './app.component';
import { RenderService } from './services/renderService';
import { SocketIOService } from './services/socketioService';
import { ModifierComponent } from './modifier/modifier';
import { FormsModule }   from '@angular/forms';

@NgModule({
  imports:      [ BrowserModule, FormsModule ],
  providers:    [ RenderService, SocketIOService ],
  declarations: [ AppComponent, ModifierComponent ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
