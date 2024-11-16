import { TestBed } from '@angular/core/testing';

import { MrtLibraryService } from './mrt-library.service';

describe('MrtLibraryService', () => {
  let service: MrtLibraryService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MrtLibraryService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
