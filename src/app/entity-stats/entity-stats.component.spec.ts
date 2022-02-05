import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EntityStatsComponent } from './entity-stats.component';

describe('EntityStatsComponent', () => {
  let component: EntityStatsComponent;
  let fixture: ComponentFixture<EntityStatsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EntityStatsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EntityStatsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
