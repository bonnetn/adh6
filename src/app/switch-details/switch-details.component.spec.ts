import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SwitchDetailsComponent } from './switch-details.component';

describe('SwitchDetailsComponent', () => {
  let component: SwitchDetailsComponent;
  let fixture: ComponentFixture<SwitchDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SwitchDetailsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SwitchDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
