import { Component, Input } from '@angular/core';
import { MRTScenario, MRTScenarioResponse } from '../../../types/mrt-library.type';
import { MrtLibraryService } from '../../../services/mrt-library/mrt-library.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-mrt-scenario',
  templateUrl: './mrt-scenario.component.html',
  styleUrl: './mrt-scenario.component.scss'
})
export class MrtScenarioComponent {

  @Input() mrtScenario!: MRTScenario;

  mrtScenarioResponse$!: Observable<MRTScenarioResponse>;

  constructor(
    private mrtLibraryService: MrtLibraryService,
  ) { }

  startMrtScenario() {
    this.mrtScenarioResponse$ = this.mrtLibraryService.startMrtScenario({
      id: this.mrtScenario.id,
    });
  }

}
