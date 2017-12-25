import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SwitchDetailsComponent } from './switch-details.component';

import { RouterTestingModule } from '@angular/router/testing';
import { ApiModule } from '../api/api.module';

describe('SwitchDetailsComponent', () => {
  let component: SwitchDetailsComponent;
  let fixture: ComponentFixture<SwitchDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SwitchDetailsComponent ]
      imports: [
        ApiModule,
        RouterTestingModule,
      ]
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
