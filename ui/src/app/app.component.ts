import { Component, OnInit } from '@angular/core';
import { version } from '../../package.json'
import { Observable } from 'rxjs';
import { VersionService } from './services/version/version.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {

  webappVersion: string = version;
  zettabgpVersion!: Observable<string>;

  constructor(
    private versionService: VersionService,
  ) { }

  ngOnInit(): void {
    this.zettabgpVersion = this.versionService.getVersion();
  }

}
