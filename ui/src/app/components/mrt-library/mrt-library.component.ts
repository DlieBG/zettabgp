import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { MRTLibrary } from '../../types/mrt-library.type';
import { MrtLibraryService } from '../../services/mrt-library/mrt-library.service';

@Component({
  selector: 'app-mrt-library',
  templateUrl: './mrt-library.component.html',
  styleUrl: './mrt-library.component.scss'
})
export class MrtLibraryComponent implements OnInit {

  mrtLibrary!: Observable<MRTLibrary>;

  constructor(
    private mrtLibraryService: MrtLibraryService,
  ) { }

  ngOnInit(): void {
    this.mrtLibrary = this.mrtLibraryService.getMrtLibrary();
  }

}
