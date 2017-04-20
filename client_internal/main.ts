import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule }              from './app/app.module';
import "./app/utils/MathExt";

platformBrowserDynamic().bootstrapModule(AppModule);
