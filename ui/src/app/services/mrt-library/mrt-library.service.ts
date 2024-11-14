import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { MRTLibrary, MRTScenarioRequest, MRTScenarioResponse } from '../../types/mrt-library.type';

@Injectable({
  providedIn: 'root'
})
export class MrtLibraryService {

  constructor(
    private httpClient: HttpClient,
  ) { }

  get_mrt_library(): Observable<MRTLibrary> {
    return this.httpClient.get<MRTLibrary>('api/mrt-library');
  }

  start_mrt_library(mrtScenarioRequest: MRTScenarioRequest): Observable<MRTScenarioResponse> {
    return this.httpClient.post<MRTScenarioResponse>('api/mrt-library', mrtScenarioRequest);
  }

}
