import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MrtLibraryComponent } from './mrt-library.component';

describe('MrtLibraryComponent', () => {
  let component: MrtLibraryComponent;
  let fixture: ComponentFixture<MrtLibraryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MrtLibraryComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MrtLibraryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
