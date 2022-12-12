//
// Created by god on 12.12.2022.
//

#include "Projectile.h"
#include "punity/Components/PCollider.h"
#include <cmath>

namespace Game {

    void Projectile::on_start_collision(Punity::Components::PCollider *other) {
        // I simply destroy the projectile on hit. Others have to deal with
        // whatever they want to do if hit by projectiles.
        // I also support an exception, however. If we shoot from inside the player,
        // I may not want it to be destroyed instantly.

        std::cout << "Hit with " << other->get_entity()->get_name() << ' ' << (int)other->information << " and have exp " << (int)self << '\n';
        if (other->information == exception || other->information == self) return;

        get_entity()->destroy();
    }

    Projectile* Projectile::set_target_point(Punity::Utils::PVector target_point) {
        // Compute line and get its normalized vector
        Punity::Utils::PVector current_position = get_entity()->get_transform()->global_position;

        // Offset by current position. This means we treat current position as (0, 0)
        target_point -= current_position;

        // Get the normalized point sitting on the circle.
        // Offset by pi/2
        float radians = -std::atan2(target_point.y, target_point.x) + 1.57079632679f;
        direction = {std::sin(radians) , std::cos(radians)};

        std::cout << radians << direction << target_point << current_position << '\n';

        return this;
    }

    void Projectile::on_update() {
        // Simply translate, nothing special
        get_entity()->get_transform()->translate(direction * speed * Punity::Time.delta_time);
    }

    Projectile *Projectile::set_exception(uint8_t exp) {
        exception = exp;
        return this;
    }

    Projectile *Projectile::set_self(uint8_t _self) {
        self = _self;
        return this;
    }
}