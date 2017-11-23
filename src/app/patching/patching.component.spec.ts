import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PatchingComponent } from './patching.component';

describe('PatchingComponent', () => {
  let component: PatchingComponent;
  let fixture: ComponentFixture<PatchingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PatchingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PatchingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
