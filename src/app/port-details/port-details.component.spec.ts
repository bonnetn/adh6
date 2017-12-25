import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PortDetailsComponent } from './port-details.component';
import { ApiModule } from '../api/api.module';
import { RouterTestingModule } from '@angular/router/testing';

describe('PortDetailsComponent', () => {
  let component: PortDetailsComponent;
  let fixture: ComponentFixture<PortDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PortDetailsComponent ]
      imports: [
        ApiModule,
        RouterTestingModule,
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PortDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
